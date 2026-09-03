from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Program, ProgramCategory, SystemConfig
from .oos_helper import get_video_url, get_video_url2
from .services.cards import build_home_cards


def index(request):
    now = timezone.now()
    config = SystemConfig.get_current_config()
    week_number = SystemConfig.get_current_week_number()
    is_odd_week = SystemConfig.is_odd_week()

    context = {
        "current_date": now,
        "week_number": week_number,
        "is_odd_week": is_odd_week,
        "cards": build_home_cards(now, is_odd_week),
        "semester_name": config.semester_name,
        "first_week_date": config.first_week_start_date,
    }
    return render(request, "index.html", context)


def program_history(request, category_id):
    category = get_object_or_404(ProgramCategory, id=category_id)
    programs = Program.objects.filter(
        category=category,
        is_active=True,
    ).order_by("-publish_date")
    config = SystemConfig.get_current_config()

    context = {
        "category": category,
        "programs": programs,
        "semester_name": config.semester_name,
    }
    return render(request, "program_history.html", context)


def video_player(request):
    context = {
        "video_url": get_video_url(expires=72000),
        "video_title": "室内运动视频",
    }
    return render(request, "video_player.html", context)


def video_player2(request):
    context = {
        "video_url": get_video_url2(expires=72000),
        "video_title": "朝会思政",
    }
    return render(request, "video_player.html", context)
