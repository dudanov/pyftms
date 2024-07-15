import io

from pyftms.serializer import NumSerializer, get_serializer

_NUM_TESTS: tuple[tuple[str, int | float, bytes], ...] = (
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
)


def _test(fmt: str, num: int | float, buf: bytes):
    s = get_serializer(fmt)

    assert isinstance(s, NumSerializer)
    assert s.deserialize(buf) == num

    bio = io.BytesIO()

    assert s.serialize(bio, num) == s.get_size()
    assert bio.getvalue() == buf


def test_num_serializer():
    for data in _NUM_TESTS:
        _test(*data)
