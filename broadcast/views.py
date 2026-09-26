from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Program, ProgramCategory
from .services.cards import build_home_cards
from .services.oss import get_signed_video_url
from .services.schedule import get_semester_state


def index(request):
    now = timezone.now()
    semester = get_semester_state(now)

    context = {
        "current_date": now,
        "week_number": semester.week_number,
        "is_odd_week": semester.is_odd_week,
        "semester_has_started": semester.has_started,
        "cards": build_home_cards(now, semester.is_odd_week),
        "semester_name": semester.config.semester_name,
        "first_week_date": semester.config.first_week_start_date,
    }
    return render(request, "index.html", context)


def program_history(request, category_id):
    category = get_object_or_404(ProgramCategory, id=category_id)
    programs = Program.objects.filter(
        category=category,
        is_active=True,
    ).order_by("-publish_date")
    semester = get_semester_state()

    context = {
        "category": category,
        "programs": programs,
        "semester_name": semester.config.semester_name,
    }
    return render(request, "program_history.html", context)


def video_player(request):
    return _render_video(request, "primary", "室内运动视频")


def video_player2(request):
    return _render_video(request, "secondary", "朝会思政")


def _render_video(request, slot, title):
    context = {"video_title": title, "video_url": "", "video_error": ""}
    try:
        context["video_url"] = get_signed_video_url(slot=slot, expires=72000)
        status = 200
    except ImproperlyConfigured:
        context["video_error"] = "视频暂未配置，请联系管理员。"
        status = 503
    return render(request, "video_player.html", context, status=status)
