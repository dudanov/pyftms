import io

import pytest

from pyftms.serializer import FtmsNumbers, NumSerializer, get_serializer


@pytest.mark.parametrize(
    "format,number,result",
    [
        ("u1", 128, b"\x80"),
        ("u2", 128, b"\x80\x00"),
        ("u3", 128, b"\x80\x00\x00"),
        ("u1.1", 12.8, b"\x80"),
        ("u2.1", 12.8, b"\x80\x00"),
        ("u3.1", 12.8, b"\x80\x00\x00"),
        ("s1", -128, b"\x80"),
        ("s2", -128, b"\x80\xff"),
        ("s3", -128, b"\x80\xff\xff"),
        ("s1.1", -12.8, b"\x80"),
        ("s2.1", -12.8, b"\x80\xff"),
        ("s3.1", -12.8, b"\x80\xff\xff"),
        ("u2", None, b"\xff\xff"),
        ("u2.1", None, b"\xff\xff"),
        ("s2", None, b"\xff\x7f"),
        ("s2.1", None, b"\xff\x7f"),
    ],
)
def test_num_serializer(format: str, number: FtmsNumbers, result: bytes):
    serializer = get_serializer(format)

    assert isinstance(serializer, NumSerializer)
    assert serializer.deserialize(result) == number

    bio = io.BytesIO()

    size = serializer.serialize(bio, number)
    assert size == serializer.get_size() and size == len(result)
    assert bio.getvalue() == result
