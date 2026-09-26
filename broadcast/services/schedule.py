"""Semester calendar calculations used by views and card builders."""

from collections import namedtuple
from datetime import datetime, timedelta

from django.utils import timezone

from broadcast.models import SystemConfig


class SemesterState(namedtuple("SemesterStateBase", "config current_date week_number")):
    """Immutable semester state, compatible with the original Python 3.6 runtime."""

    __slots__ = ()

    @property
    def is_odd_week(self):
        return self.week_number > 0 and self.week_number % 2 == 1

    @property
    def has_started(self):
        return self.week_number > 0


def week_number_for(current_date, first_week_start_date):
    """Return the one-based school week, or 0 before the semester starts."""
    if current_date < first_week_start_date:
        return 0
    return ((current_date - first_week_start_date).days // 7) + 1


def get_semester_state(at=None):
    config = SystemConfig.get_current_config()
    current_date = _local_date(at)
    return SemesterState(
        config=config,
        current_date=current_date,
        week_number=week_number_for(current_date, config.first_week_start_date),
    )


def next_program_date(current, day_of_week):
    """Keep the legacy update-calendar rule while making it independently testable."""
    current_date = _local_date(current)
    python_day_of_week = day_of_week - 1
    days_ahead = python_day_of_week - current_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    # Tuesday programs are published for the following rotation.
    if day_of_week == 2:
        days_ahead += 7

    return current_date + timedelta(days=days_ahead)


def _local_date(value=None):
    if value is None:
        return timezone.localdate()
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            return timezone.localtime(value).date()
        return value.date()
    return value
