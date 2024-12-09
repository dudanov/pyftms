import pytest

from pyftms.models import MachineStatusModel, TreadmillData
from pyftms.serializer import BaseModel, ModelSerializer, get_serializer


@pytest.mark.parametrize(
    "model,data,result",
    [
        (
            TreadmillData,
            b"\x00\x00\x00\x00",
            {"speed_instant": 0},
        ),
        # Testing `hassio-ftms` issue #3: https://github.com/dudanov/hassio-ftms/issues/3
        (
            TreadmillData,
            b"\x9c\x25\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            {
                "speed_instant": 0,
                "distance_total": 0,
                "heart_rate": 0,
                "time_elapsed": 0,
                "step_count": 0,
                "inclination": 0,
                "ramp_angle": 0,
                "elevation_gain_positive": 0,
                "elevation_gain_negative": 0,
                "energy_total": 0,
                "energy_per_hour": 0,
                "energy_per_minute": 0,
            },
        ),
        (
            MachineStatusModel,
            b"\x05\x69\x00",
            {"code": 5, "target_speed": 1.05},
        ),
    ],
)
def test_realtime_data(model: type[BaseModel], data: bytes, result: dict):
    s = get_serializer(model)

    assert isinstance(s, ModelSerializer)
    assert s.deserialize(data)._asdict() == result
