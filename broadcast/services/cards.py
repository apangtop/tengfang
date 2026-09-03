import datetime

from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse

from broadcast.models import BroadcastCard, Program, ProgramCategory


SPECIAL_PROGRAM_NAMES = ["唐宋八大家", "大唐诗人传"]
DAY_NAMES = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五"}


def next_program_date(current_date, day_of_week):
    python_day_of_week = day_of_week - 1
    days_ahead = python_day_of_week - current_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    if day_of_week == 2:
        days_ahead += 7

    return (current_date + datetime.timedelta(days=days_ahead)).date()


def build_home_cards(now, is_odd_week):
    configured_cards = _configured_cards(now)
    if configured_cards:
        return configured_cards
    return _legacy_cards(now, is_odd_week)


def _configured_cards(now):
    try:
        cards = list(
            BroadcastCard.objects.filter(is_active=True)
            .select_related("category")
            .order_by("sort_order", "id")
        )
    except (OperationalError, ProgrammingError):
        return []

    return [card for card in (_build_card_data(card, now) for card in cards) if card]


def _build_card_data(card, now):
    latest_program = None
    programs = []

    if card.category_id:
        latest_program = _latest_program(card.category)
        programs = list(
            Program.objects.filter(category=card.category, is_active=True)
            .order_by("-publish_date")
        )

    action_url = _action_url(card, latest_program)
    if card.card_type in [BroadcastCard.TYPE_LATEST_PROGRAM, BroadcastCard.TYPE_DIRECT_LINK] and not action_url:
        return None

    return {
        "id": card.id,
        "title": card.title,
        "subtitle": card.subtitle,
        "description": card.description,
        "icon_class": card.icon_class,
        "color": _normalize_color(card.color),
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
            meta.append(("当前节目日期", _format_date(latest_program.publish_date)))
            meta.append(("下次更新日期", _format_date(next_program_date(now, card.category.day_of_week))))
        if card.category.current_week_label():
            meta.append(("周次类型", card.category.current_week_label()))
    elif card.card_type == BroadcastCard.TYPE_VIDEO_ONE:
        meta.append(("节目名称", "室内课间操"))
    elif card.card_type == BroadcastCard.TYPE_VIDEO_TWO:
        meta.append(("节目名称", "朝会思政"))
    return meta


def _legacy_cards(now, is_odd_week):
    cards = []
    categories = _legacy_categories(is_odd_week)
    for category in categories:
        latest_program = _latest_program(category)
        if not latest_program:
            continue

        cards.append({
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
                ("下次更新日期", _format_date(next_program_date(now, category.day_of_week))),
            ],
        })

    cards.extend(_legacy_collection_cards())
    cards.extend(_legacy_video_cards())
    return cards


def _legacy_categories(is_odd_week):
    names = SPECIAL_PROGRAM_NAMES
    monday_categories = ProgramCategory.objects.filter(day_of_week=1).exclude(name__in=names)
    if is_odd_week:
        other_categories = ProgramCategory.objects.filter(
            day_of_week__in=[2, 4],
            is_biweekly=False,
        ).exclude(name__in=names)
    else:
        other_categories = ProgramCategory.objects.filter(
            day_of_week__in=[2, 4],
            is_biweekly=True,
        ).exclude(name__in=names)

    categories = list(monday_categories) + list(other_categories)
    return sorted(categories, key=lambda category: category.day_of_week)


def _legacy_collection_cards():
    cards = []
    for name, color, icon in [
        ("唐宋八大家", "emerald", "fa-book-open"),
        ("大唐诗人传", "amber", "fa-feather"),
    ]:
        try:
            category = ProgramCategory.objects.get(name=name)
        except ProgramCategory.DoesNotExist:
            continue

        programs = list(
            Program.objects.filter(category=category, is_active=True)
            .order_by("-publish_date")
        )
        cards.append({
            "id": f"legacy-collection-{category.id}",
            "title": "晚读经典赏析",
            "subtitle": name,
            "description": f"共 {len(programs)} 集节目",
            "icon_class": icon,
            "color": _normalize_color(category.color or color),
            "button_text": "浏览所有节目",
            "action_url": "",
            "latest_program": None,
            "show_latest_program": False,
            "category": category,
            "programs": programs,
            "opens_modal": True,
            "modal_id": f"legacy-modal-{category.id}",
            "meta": [("节目名称", name), ("节目数量", f"{len(programs)} 集")],
        })
    return cards


def _legacy_video_cards():
    return [
        {
            "id": "video-one",
            "title": "课间操视频",
            "subtitle": "室内课间操",
            "description": "固定视频入口",
            "icon_class": "fa-chalkboard-teacher",
            "color": "blue",
            "button_text": "播放视频",
            "action_url": reverse("video_player"),
            "latest_program": None,
            "show_latest_program": False,
            "category": None,
            "programs": [],
            "opens_modal": False,
            "modal_id": "",
            "meta": [("节目名称", "室内课间操")],
        },
        {
            "id": "video-two",
            "title": "朝会思政",
            "subtitle": "思想政治教育",
            "description": "固定视频入口",
            "icon_class": "fa-flag",
            "color": "rose",
            "button_text": "播放本周节目",
            "action_url": reverse("video_player2"),
            "latest_program": None,
            "show_latest_program": False,
            "category": None,
            "programs": [],
            "opens_modal": False,
            "modal_id": "",
            "meta": [("节目名称", "朝会思政"), ("更新周期", "定期播放")],
        },
    ]


def _latest_program(category):
    return (
        Program.objects.filter(category=category, is_active=True)
        .order_by("-publish_date")
        .first()
    )


def _normalize_color(color):
    color_map = {
        "blue": "blue",
        "indigo": "indigo",
        "purple": "purple",
        "green": "emerald",
        "emerald": "emerald",
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


def _format_date(value):
    return value.strftime("%Y年%m月%d日")
