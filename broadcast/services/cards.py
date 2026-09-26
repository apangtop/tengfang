"""Build the presentation data consumed by the homepage template."""

from django.db.models import Prefetch
from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse

from broadcast.models import BroadcastCard, Program, ProgramCategory
from broadcast.services.programs import (
    SPECIAL_PROGRAM_NAMES,
    active_programs,
    latest_active_program,
    legacy_categories_for_week,
)
from broadcast.services.schedule import next_program_date

DAY_NAMES = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五"}


def build_home_cards(now, is_odd_week):
    """Use configured cards when available and retain the pre-card legacy fallback."""
    configured = _configured_cards(now, is_odd_week)
    if configured is not None:
        return configured
    return _legacy_cards(now, is_odd_week)


def _configured_cards(now, is_odd_week):
    active_program_queryset = Program.objects.filter(is_active=True).order_by(
        "-publish_date", "-id"
    )
    try:
        all_cards_exist = BroadcastCard.objects.exists()
        cards = list(
            BroadcastCard.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch(
                    "category__programs",
                    queryset=active_program_queryset,
                    to_attr="active_programs",
                )
            )
            .order_by("sort_order", "id")
        )
    except (OperationalError, ProgrammingError):
        return None

    if not all_cards_exist:
        return None

    return [
        card_data
        for card in cards
        if _should_display_card(card, is_odd_week)
        for card_data in [_build_card_data(card, now)]
        if card_data
    ]


def _build_card_data(card, now):
    programs = active_programs(card.category) if card.category_id else []
    latest_program = programs[0] if programs else None
    action_url = _action_url(card, latest_program)

    if (
        card.card_type
        in (
            BroadcastCard.TYPE_LATEST_PROGRAM,
            BroadcastCard.TYPE_DIRECT_LINK,
        )
        and not action_url
    ):
        return None

    return {
        "id": card.id,
        "title": card.title,
        "subtitle": card.subtitle,
        "description": card.description,
        "icon_class": card.icon_class,
        "color": _resolve_card_color(card),
        "button_text": card.button_text,
        "action_url": action_url,
        "latest_program": latest_program,
        "show_latest_program": card.show_latest_program,
        "category": card.category,
        "programs": programs,
        "opens_modal": card.card_type == BroadcastCard.TYPE_PROGRAM_LIST,
        "modal_id": f"card-modal-{card.id}",
        "meta": _card_meta(card, latest_program, now),
    }


def _action_url(card, latest_program):
    if card.card_type == BroadcastCard.TYPE_VIDEO_ONE:
        return reverse("video_player")
    if card.card_type == BroadcastCard.TYPE_VIDEO_TWO:
        return reverse("video_player2")
    if card.card_type == BroadcastCard.TYPE_DIRECT_LINK:
        return card.link_url
    if card.card_type == BroadcastCard.TYPE_LATEST_PROGRAM and latest_program:
        return latest_program.link
    return ""


def _card_meta(card, latest_program, now):
    meta = []
    if card.category:
        meta.append(("节目名称", card.category.name))
        if card.show_latest_program and latest_program:
            meta.extend(
                [
                    ("当前节目日期", _format_date(latest_program.publish_date)),
                    (
                        "下次更新日期",
                        _format_date(next_program_date(now, card.category.day_of_week)),
                    ),
                ]
            )
        if card.category.current_week_label():
            meta.append(("周次类型", card.category.current_week_label()))
    elif card.card_type == BroadcastCard.TYPE_VIDEO_ONE:
        meta.append(("节目名称", "室内课间操"))
    elif card.card_type == BroadcastCard.TYPE_VIDEO_TWO:
        meta.append(("节目名称", "朝会思政"))
    return meta


def _legacy_cards(now, is_odd_week):
    cards = []
    for category in legacy_categories_for_week(is_odd_week):
        latest_program = latest_active_program(category)
        if not latest_program:
            continue
        cards.append(
            {
                "id": f"legacy-{category.id}",
                "title": DAY_NAMES.get(category.day_of_week, "节目"),
                "subtitle": category.name,
                "description": category.description,
                "icon_class": category.icon_class,
                "color": _normalize_color(category.color),
                "button_text": "播放本周节目",
                "action_url": latest_program.link,
                "latest_program": latest_program,
                "show_latest_program": True,
                "category": category,
                "programs": [],
                "opens_modal": False,
                "modal_id": "",
                "meta": [
                    ("节目名称", category.name),
                    ("当前节目日期", _format_date(latest_program.publish_date)),
                    (
                        "下次更新日期",
                        _format_date(next_program_date(now, category.day_of_week)),
                    ),
                ],
            }
        )

    cards.extend(_legacy_collection_cards())
    cards.extend(_legacy_video_cards())
    return cards


def _legacy_collection_cards():
    cards = []
    appearances = {
        "唐宋八大家": ("emerald", "fa-book-open"),
        "大唐诗人传": ("amber", "fa-feather"),
    }
    categories = ProgramCategory.objects.filter(
        name__in=SPECIAL_PROGRAM_NAMES
    ).order_by("id")
    for category in categories:
        fallback_color, fallback_icon = appearances[category.name]
        programs = active_programs(category)
        cards.append(
            {
                "id": f"legacy-collection-{category.id}",
                "title": "晚读经典赏析",
                "subtitle": category.name,
                "description": f"共 {len(programs)} 集节目",
                "icon_class": category.icon_class or fallback_icon,
                "color": _normalize_color(category.color or fallback_color),
                "button_text": "浏览所有节目",
                "action_url": "",
                "latest_program": None,
                "show_latest_program": False,
                "category": category,
                "programs": programs,
                "opens_modal": True,
                "modal_id": f"legacy-modal-{category.id}",
                "meta": [
                    ("节目名称", category.name),
                    ("节目数量", f"{len(programs)} 集"),
                ],
            }
        )
    return cards


def _legacy_video_cards():
    return [
        _video_card(
            card_id="video-one",
            title="课间操视频",
            subtitle="室内课间操",
            icon="fa-chalkboard-teacher",
            color="blue",
            button_text="播放视频",
            route="video_player",
            meta=[("节目名称", "室内课间操")],
        ),
        _video_card(
            card_id="video-two",
            title="朝会思政",
            subtitle="思想政治教育",
            icon="fa-flag",
            color="rose",
            button_text="播放本周节目",
            route="video_player2",
            meta=[("节目名称", "朝会思政"), ("更新周期", "定期播放")],
        ),
    ]


def _video_card(*, card_id, title, subtitle, icon, color, button_text, route, meta):
    return {
        "id": card_id,
        "title": title,
        "subtitle": subtitle,
        "description": "固定视频入口",
        "icon_class": icon,
        "color": color,
        "button_text": button_text,
        "action_url": reverse(route),
        "latest_program": None,
        "show_latest_program": False,
        "category": None,
        "programs": [],
        "opens_modal": False,
        "modal_id": "",
        "meta": meta,
    }


def _normalize_color(color):
    color_map = {
        "blue": "blue",
        "indigo": "indigo",
        "purple": "purple",
        "green": "emerald",
        "emerald": "emerald",
        "pink": "pink",
        "red": "rose",
        "rose": "rose",
        "yellow": "amber",
        "orange": "amber",
        "amber": "amber",
        "gray": "slate",
        "grey": "slate",
        "slate": "slate",
    }
    return color_map.get((color or "").strip().lower(), "blue")


def _should_display_card(card, is_odd_week):
    if card.card_type != BroadcastCard.TYPE_LATEST_PROGRAM or not card.category:
        return True
    if card.category.day_of_week not in (2, 4):
        return True
    return card.category.is_biweekly != is_odd_week


def _resolve_card_color(card):
    if card.category_id and card.category and card.category.color:
        return _normalize_color(card.category.color)
    return _normalize_color(card.color)


def _format_date(value):
    return value.strftime("%Y年%m月%d日")
