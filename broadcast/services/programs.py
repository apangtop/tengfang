"""Queries for active broadcast programs."""

from broadcast.models import Program, ProgramCategory

SPECIAL_PROGRAM_NAMES = ("唐宋八大家", "大唐诗人传")


def active_programs(category):
    prefetched = getattr(category, "active_programs", None)
    if prefetched is not None:
        return prefetched
    return list(
        Program.objects.filter(category=category, is_active=True).order_by(
            "-publish_date", "-id"
        )
    )


def latest_active_program(category):
    programs = active_programs(category)
    return programs[0] if programs else None


def legacy_categories_for_week(is_odd_week):
    monday_categories = ProgramCategory.objects.filter(day_of_week=1).exclude(
        name__in=SPECIAL_PROGRAM_NAMES
    )
    rotating_categories = ProgramCategory.objects.filter(
        day_of_week__in=(2, 4),
        is_biweekly=not is_odd_week,
    ).exclude(name__in=SPECIAL_PROGRAM_NAMES)
    return sorted(
        [*monday_categories, *rotating_categories],
        key=lambda category: (category.day_of_week, category.name, category.pk),
    )
