# Copyright 2024-2025, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

# REAL-TIME TRAINING DATA

CADENCE_AVERAGE = "cadence_average"
CADENCE_INSTANT = "cadence_instant"
DISTANCE_TOTAL = "distance_total"
ELEVATION_GAIN_NEGATIVE = "elevation_gain_negative"
ELEVATION_GAIN_POSITIVE = "elevation_gain_positive"
ENERGY_PER_HOUR = "energy_per_hour"
ENERGY_PER_MINUTE = "energy_per_minute"
ENERGY_TOTAL = "energy_total"
FORCE_ON_BELT = "force_on_belt"
HEART_RATE = "heart_rate"
INCLINATION = "inclination"
INDOOR_BIKE_SIMULATION = "indoor_bike_simulation"
METABOLIC_EQUIVALENT = "metabolic_equivalent"
MOVEMENT_DIRECTION = "movement_direction"
PACE_AVERAGE = "pace_average"
PACE_INSTANT = "pace_instant"
POWER_AVERAGE = "power_average"
POWER_INSTANT = "power_instant"
POWER_OUTPUT = "power_output"
RAMP_ANGLE = "ramp_angle"
RESISTANCE_LEVEL = "resistance_level"
SPEED_AVERAGE = "speed_average"
SPEED_INSTANT = "speed_instant"
SPLIT_TIME_AVERAGE = "split_time_average"
SPLIT_TIME_INSTANT = "split_time_instant"
STEP_COUNT = "step_count"
STEP_RATE_AVERAGE = "step_rate_average"
STEP_RATE_INSTANT = "step_rate_instant"
STRIDE_COUNT = "stride_count"
STROKE_COUNT = "stroke_count"
STROKE_RATE_AVERAGE = "stroke_rate_average"
STROKE_RATE_INSTANT = "stroke_rate_instant"
TIME_ELAPSED = "time_elapsed"
TIME_REMAINING = "time_remaining"
TRAINING_STATUS = "training_status"

# TARGET SETTINGS ATTRIBUTES

# WITH RANGES

# Optional

TARGET_SPEED = "target_speed"
TARGET_POWER = "target_power"
TARGET_HEART_RATE = "target_heart_rate"
TARGET_INCLINATION = "target_inclination"
TARGET_RESISTANCE = "target_resistance"

# WITHOUT RANGES

# Mandatory

RESET = "reset"
START = "start"
STOP = "stop"
PAUSE = "pause"

# Optional

BIKE_SIMULATION = "bike_simulation"
SPIN_DOWN = "spin_down"
TARGET_CADENCE = "target_cadence"
TARGET_DISTANCE = "target_distance"
TARGET_ENERGY = "target_energy"
TARGET_STEPS = "target_steps"
TARGET_STRIDES = "target_strides"
TARGET_TIME = "target_time"
TARGET_TIME_TWO_ZONES = "target_time_two_zones"
TARGET_TIME_TIME_THREE_ZONES = "target_time_three_zones"
TARGET_TIME_TIME_FIVE_ZONES = "target_time_five_zones"
WHEEL_CIRCUMFERENCE = "wheel_circumference"

# Bluetooth FTMS UUIDs

FTMS_UUID = "1826"
"""Fitness Machine Service"""

FEATURE_UUID = "2acc"
"""
`Requirement`: Mandatory.
`Property`: Read.
`Device Type`: Treadmill, walking pad, elliptical machine, rower, and smart bike.
`Description`: Describes the capabilities supported by the device.
"""

TREADMILL_DATA_UUID = "2acd"
"""
`Requirement`: Optional.
`Property`: Notify.
`Device Type`: Treadmill and walking pad only.
`Description`: Reports real-time workout data.
"""

CROSS_TRAINER_DATA_UUID = "2ace"
"""
`Requirement`: Optional.
`Property`: Notify.
`Device Type`: Elliptical machines only.
`Description`: Reports real-time workout data.
"""

ROWER_DATA_UUID = "2ad1"
"""
`Requirement`: Optional.
`Property`: Notify.
`Device Type`: Rower only.
`Description`: Reports real-time workout data.
"""

INDOOR_BIKE_DATA_UUID = "2ad2"
"""
`Requirement`: Optional.
`Property`: Notify.
`Device Type`: Smart bike only.
`Description`: Reports real-time workout data.
"""

TRAINING_STATUS_UUID = "2ad3"
"""
`Requirement`: Optional.
`Property`: Read/Notify.
`Device Type`: Treadmill, walking pad, elliptical machine, rower, and smart bike.
`Description`: Reports the device status data.
"""

SPEED_RANGE_UUID = "2ad4"
"""
`Requirement`: Mandatory if the `Speed Target Setting` feature is supported; otherwise Optional.
`Property`: Read.
`Device Type`: Treadmill, walking pad, and smart bike.
`Description`: Reports the supported speed range.
"""

INCLINATION_RANGE_UUID = "2ad5"
"""
`Requirement`: Mandatory if the `Inclination Target Setting` feature is supported; otherwise Optional.
`Property`: Read.
`Device Type`: Treadmill and walking pad.
`Description`: Reports the supported inclination range.
"""

RESISTANCE_LEVEL_RANGE_UUID = "2ad6"
"""
`Requirement`: Mandatory if the `Resistance Target Setting` feature is supported; otherwise Optional.
`Property`: Read.
`Device Type`: Elliptical machine.
`Description`: Reports the supported resistance level range.
"""

HEART_RATE_RANGE_UUID = "2ad7"
"""
`Requirement`: Mandatory if the `Heart Rate Target Setting` feature is supported; otherwise Optional.
`Property`: Read.
`Device Type`: Treadmill, walking pad, elliptical machine, rower, and smart bike.
`Description`: Reports supported heart rate range.
"""

POWER_RANGE_UUID = "2ad8"
"""
`Requirement`: Mandatory if the `Power Target Setting` feature is supported; otherwise Optional.
`Property`: Read.
`Device Type`: Elliptical machine, rower, and smart bike.
`Description`: Reports the supported power range.
"""

CONTROL_POINT_UUID = "2ad9"
"""
`Requirement`: Optional.
`Property`: Write/Indicate.
`Device Type`: Optional support for treadmills and walking pads, and mandatory for elliptical machines, rowers, and smart bikes.
`Description`: Controls the status (paused or resumed) of fitness machine.
"""

STATUS_UUID = "2ada"
"""
`Requirement`: Mandatory if the `Fitness Machine Control Point` is supported; otherwise Optional.
`Property`: Notify.
`Device Type`: Treadmill, walking pad, elliptical machine, rower, and smart bike.
`Description`: Reports workout status changes of the fitness machine.
"""
