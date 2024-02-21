import datetime

from lambdas.utils import dt_utils


def test_datetime_from_millis():
    assert dt_utils.datetime_from_millis(1708412767000) == datetime.datetime(
        2024, 2, 20, 7, 6, 7, tzinfo=datetime.timezone.utc)
    assert dt_utils.datetime_from_millis(1708449769000) == datetime.datetime(
        2024, 2, 20, 17, 22, 49, tzinfo=datetime.timezone.utc)


def test_datetime_from_seconds():
    assert dt_utils.datetime_from_seconds(1708412767) == datetime.datetime(
        2024, 2, 20, 7, 6, 7, tzinfo=datetime.timezone.utc)
    assert dt_utils.datetime_from_seconds(1708449769) == datetime.datetime(
        2024, 2, 20, 17, 22, 49, tzinfo=datetime.timezone.utc)
