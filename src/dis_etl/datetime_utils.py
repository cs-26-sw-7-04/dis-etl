"""
Transform layer for dim_datetime: turns a UTC-aware datetime into the
full set of fields needed for a dim_datetime row.
"""
import datetime
from zoneinfo import ZoneInfo


CPH = ZoneInfo("Europe/Copenhagen")


_LECTURE_SLOTS = {'0815_1000', '1015_1200', '1230_1415', '1430_1615'}
_BREAK_SLOTS = {'1000_1015', '1200_1230', '1415_1430'}


_BANDS = [
    (0,            8 * 60 + 15,  '0000_0815'),
    (8 * 60 + 15,  10 * 60,      '0815_1000'),
    (10 * 60,      10 * 60 + 15, '1000_1015'),
    (10 * 60 + 15, 12 * 60,      '1015_1200'),
    (12 * 60,      12 * 60 + 30, '1200_1230'),
    (12 * 60 + 30, 14 * 60 + 15, '1230_1415'),
    (14 * 60 + 15, 14 * 60 + 30, '1415_1430'),
    (14 * 60 + 30, 16 * 60 + 15, '1430_1615'),
    (16 * 60 + 15, 24 * 60,      '1615_2400'),
]


def truncate_to_minute(dt: datetime.datetime) -> datetime.datetime:
    """Truncate a timestamp to the starting minute"""
    return dt.replace(second=0, microsecond=0)


def classify_timeslot(hour: int, minute: int) -> str:
    """Time into timeslot in the day"""
    total_minutes = hour * 60 + minute
    for start, end, label in _BANDS:
        if start <= total_minutes < end:
            return label
    return '1615_2400'  # fallback, shouldn't be reached


def classify_timeslot_type(timeslot: str) -> str:
    """Timeslot into type"""
    if timeslot in _LECTURE_SLOTS:
        return 'lecture'
    if timeslot in _BREAK_SLOTS:
        return 'break'
    return 'outside_schedule'


def decompose_datetime(dt_utc: datetime.datetime) -> dict:
    """
    Given a UTC-aware datetime, return a dict matching dim_datetime's 
    attribute set
    """
    dt_utc = truncate_to_minute(dt_utc)
    local = dt_utc.astimezone(CPH)
    timeslot = classify_timeslot(local.hour, local.minute)

    return {
        'timestamp_utc': dt_utc,
        'year': local.year,
        'month': local.month,
        'month_name': local.strftime('%B'),
        'week': local.isocalendar().week,
        'weekday': local.strftime('%A'),
        'day': local.day,
        'hour': local.hour,
        'minute': local.minute,
        'timeslot': timeslot,
        'timeslot_type': classify_timeslot_type(timeslot),
    }
