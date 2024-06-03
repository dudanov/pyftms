# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
import io
from types import GenericAlias, MappingProxyType, UnionType
from typing import (
    Any,
    ClassVar,
    Generic,
    Iterator,
    Optional,
    Self,
    TypedDict,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    overload,
    override,
)

from .list import ListSerializer
from .num import NumSerializer
from .serializer import Serializer


class ModelMeta(TypedDict, total=False):
    format: str
    features_bit: int
    code: int
    num: int


def model_meta(
    *,
    format: str = "",
    features_bit: int | None = None,
    code: int | None = None,
    num: int | None = None,
) -> ModelMeta:
    result = ModelMeta(format=format)

    if features_bit is not None:
        result["features_bit"] = features_bit

    if code is not None:
        result["code"] = code

    if num is not None:
        result["num"] = num

    return result


def _get_model_field_serializer(field: dc.Field):
    meta, type_ = cast(ModelMeta, field.metadata), field.type

    if get_origin(type_) in (Optional, Union, UnionType):
        if (type_ := get_args(type_)[0]) is None:
            raise TypeError("Failed to get first type.")

    if isinstance(type_, TypeVar):
        if (type_ := type_.__bound__) is None:
            raise TypeError("'TypeVar' must have bound type.")

    def _get_serializer(type_) -> Serializer:
        if issubclass(type_, (int, float)):
            if fmt := meta.get("format"):
                return get_serializer(fmt)

            raise TypeError(f"Format string for field '{field.name}' is required.")

        if issubclass(type_, BaseModel):
            return get_serializer(type_)

        if isinstance(type_, GenericAlias):
            if (num := meta.get("num")) is None:
                raise TypeError("Number of elements is required.")

            serializer = _get_serializer(get_args(type_)[0])

            return ListSerializer(serializer, num)

        raise TypeError("Unsupported type.")

    return _get_serializer(type_)


def _get_model_serializers(cls: type["BaseModel"]) -> MappingProxyType[str, Serializer]:
    """Generate tuples of Fields and its Serializers."""
    if (serializers_ := getattr(cls, "_model_serializers", None)) is None:
        result: dict[str, Serializer] = {}

        for field in dc.fields(cls):
            if field.metadata:
                result[field.name] = _get_model_field_serializer(field)

        setattr(cls, "_model_serializers", serializers_ := MappingProxyType(result))

    return serializers_


@dc.dataclass(frozen=True)
class BaseModel:
    _model_serializers: ClassVar[MappingProxyType[str, Serializer]]

    @classmethod
    def _iter_fields_serializers(cls) -> Iterator[tuple[dc.Field, Serializer]]:
        """Generate tuples of Fields and its Serializers."""
        serializers = _get_model_serializers(cls)

        for field in dc.fields(cls):
            if (serializer := serializers.get(field.name)) is not None:
                yield field, serializer

    @classmethod
    def _deserialize_asdict(cls, src: io.IOBase) -> dict[str, Any]:
        kwargs = {}

        for field, serializer in cls._iter_fields_serializers():
            value, type_ = serializer._deserialize(src), field.type

            if value is None:
                continue

            if get_origin(type_) in (Optional, Union, UnionType):
                if (type_ := get_args(type_)[0]) is None:
                    raise TypeError("Failed to get first type.")

            if isinstance(serializer, (NumSerializer, ListSerializer)):
                value = type_(value)

            kwargs[field.name] = value

        return kwargs

    @classmethod
    def _deserialize(cls, src: io.IOBase) -> Self:
        return cls(**cls._deserialize_asdict(src))

    def _serialize(self, dst: io.IOBase) -> int:
        written = 0

        for field, serializer in self._iter_fields_serializers():
            if (val := getattr(self, field.name)) is not None:
                written += serializer.serialize(dst, val)

        return written

    @classmethod
    def _calc_size(cls) -> int:
        return sum(s.get_size() for _, s in cls._iter_fields_serializers())

    def _asdict(self, *, nested: bool = False):
        def _transform(input: dict):
            for key in tuple(input.keys()):
                if (value := input[key]) is None:
                    input.pop(key)

                elif isinstance(value, dict):
                    _transform(value)

                    if not nested:
                        input.pop(key)
                        input |= value

        _transform(result := dc.asdict(self))

        return result

    @classmethod
    def _get_features(cls, features: int) -> tuple[str, ...]:
        result = []

        def _get_cls_features(cls):
            for field in dc.fields(cls):
                meta, tp = cast(ModelMeta, field.metadata), field.type

                if not meta or field.name == "code":
                    continue

                if get_origin(tp) in (Optional, Union, UnionType):
                    if (tp := get_args(tp)[0]) is None:
                        raise TypeError("Failed to get first type.")

                if (bit := meta.get("features_bit")) is None or features & (1 << bit):
                    if isinstance(tp, type) and issubclass(tp, BaseModel):
                        _get_cls_features(tp)
                        continue

                    result.append(field.name)

        _get_cls_features(cls)

        return tuple(result)

    def __post_init__(self, *args, **kwargs):
        for field in dc.fields(self):
            if (val := getattr(self, field.name)) is None:
                continue

            meta = cast(ModelMeta, field.metadata)

            if (num := meta.get("num")) and len(val) != num:
                raise ValueError(f"Length of field '{field.name}' must be {num}.")

    @classmethod
    def _get_serializer(cls) -> Serializer[Self]:
        return get_serializer(cls)


# MODEL SERIALIZER

BaseModelT = TypeVar("BaseModelT", bound="BaseModel")


class ModelSerializer(Generic[BaseModelT], Serializer[BaseModelT]):
    """Model Serializer"""

    def __init__(self, cls: type[BaseModelT]) -> None:
        self._cls = cls

    @override
    def _deserialize(self, src: io.IOBase) -> BaseModelT:
        return self._cls._deserialize(src)

    @override
    def serialize(self, writer: io.IOBase, value: BaseModelT) -> int:
        return value._serialize(writer)

    @override
    def get_size(self) -> int:
        return self._cls._calc_size()


# SERIALIZERS REGISTRY

_registry: dict[str | type[BaseModel], Serializer] = {}
"""Serializers Registry"""


@overload
def get_serializer(arg: str, num: None = None) -> NumSerializer: ...


@overload
def get_serializer(
    arg: type[BaseModelT], num: None = None
) -> ModelSerializer[BaseModelT]: ...


@overload
def get_serializer(arg: str, num: int) -> ListSerializer[NumSerializer]: ...


@overload
def get_serializer(
    arg: type[BaseModelT], num: int
) -> ListSerializer[ModelSerializer[BaseModelT]]: ...


def get_serializer(arg: str | type[BaseModel], num: int | None = None):
    if (serializer := _registry.get(arg)) is None:
        if isinstance(arg, str):
            serializer = NumSerializer(arg)

        elif isinstance(arg, type) and issubclass(arg, BaseModel):
            serializer = ModelSerializer(arg)

        else:
            raise TypeError(f"Unsupported type {arg}.")

        _registry[arg] = serializer

    return serializer if num is None else ListSerializer(serializer, num)
