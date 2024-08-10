import pytest

from pyftms.models import TreadmillData
from pyftms.serializer import BaseModel, ModelSerializer, get_serializer


@pytest.mark.parametrize(
    "model,data,result",
    [
        (
            TreadmillData,
            b"\x00\x00\x00\x00",
            {"speed_instant": 0},
        ),
    ],
)
def test_realtime_data(model: type[BaseModel], data: bytes, result: dict):
    s = get_serializer(model)

    assert isinstance(s, ModelSerializer)
    assert s.deserialize(data)._asdict() == result
