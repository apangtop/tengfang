from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import datetime
from .models import ProgramCategory, Program, SystemConfig
from .oos_helper import get_video_url, get_video_url2


def index(request):
    """首页视图，显示所有当前活跃的节目"""
    # 获取当前日期和周次
    now = timezone.now()
    week_number = SystemConfig.get_current_week_number()
    is_odd_week = SystemConfig.is_odd_week()

    # 准备所有节目数据
    weekly_programs = []

    # 定义我们要特殊处理的节目名称（不作为常规节目显示）
    special_program_names = ['唐宋八大家', '大唐诗人传']

    # 1. 获取周一的所有节目（周一节目不受单双周影响）
    monday_categories = ProgramCategory.objects.filter(
        day_of_week=1
    ).exclude(
        name__in=special_program_names
    )

    # 2. 获取周二和周四的节目（根据单双周筛选）
    if is_odd_week:
        # 单周：显示非双周轮播的节目
        other_categories = ProgramCategory.objects.filter(
            day_of_week__in=[2, 4],
            is_biweekly=False
        ).exclude(
            name__in=special_program_names
        )
    else:
        # 双周：显示双周轮播的节目
        other_categories = ProgramCategory.objects.filter(
            day_of_week__in=[2, 4],
            is_biweekly=True
        ).exclude(
            name__in=special_program_names
        )

    # 合并所有要显示的节目类别
    program_categories = list(monday_categories) + list(other_categories)
    program_categories.sort(key=lambda x: x.day_of_week)  # 按星期排序

    # 处理所有符合条件的节目类别
    for category in program_categories:
        # 获取该类别最新的活跃节目
        latest_program = Program.objects.filter(
            category=category,
            is_active=True
        ).order_by('-publish_date').first()

        if latest_program:
            # 计算下次更新日期
            next_date = next_program_date(now, category.day_of_week)

            # 星期名称映射
            day_names = {1: "周一", 2: "周二", 4: "周四"}
            day_of_week = day_names.get(category.day_of_week, "未知")

            # 构建显示数据
            program_data = {
                'id': category.id,
                'name': category.name,
                'day_of_week': day_of_week,
                'color': category.color,
                'icon_class': category.icon_class,
                'title': latest_program.title,
                'current_date': latest_program.publish_date,
                'next_date': next_date,
                'play_url': latest_program.link,
                'is_biweekly': category.is_biweekly,
            }

            # 添加周类型标记（只为双周轮播的周二和周四节目添加标记）
            if category.day_of_week in [2, 4] and category.is_biweekly:
                program_data['week_type'] = '双周'
            elif category.day_of_week in [2, 4] and not category.is_biweekly:
                program_data['week_type'] = '单周'
            else:
                program_data['week_type'] = None

            weekly_programs.append(program_data)

    # 获取唐宋八大家节目（作为特殊节目处理）
    try:
        tangsong_category = ProgramCategory.objects.get(name='唐宋八大家')
        tangsong_color = tangsong_category.color  # 获取数据库中的颜色
        tangsong_programs = Program.objects.filter(
            category=tangsong_category,
            is_active=True
        ).order_by('-publish_date')
        tangsong_programs_count = tangsong_programs.count()
    except ProgramCategory.DoesNotExist:
        tangsong_programs = []
        tangsong_programs_count = 0
        tangsong_color = 'green'  # 默认颜色

    # 获取大唐诗人传节目（作为特殊节目处理）
    try:
        tang_poets_category = ProgramCategory.objects.get(name='大唐诗人传')
        tang_poets_color = tang_poets_category.color  # 获取数据库中的颜色
        tang_poets_programs = Program.objects.filter(
            category=tang_poets_category,
            is_active=True
        ).order_by('-publish_date')
        tang_poets_programs_count = tang_poets_programs.count()
    except ProgramCategory.DoesNotExist:
        tang_poets_programs = []
        tang_poets_programs_count = 0
        tang_poets_color = 'amber'  # 默认颜色

    # 获取系统配置
    config = SystemConfig.get_current_config()

    context = {
        'current_date': now,
        'week_number': week_number,
        'is_odd_week': is_odd_week,
        'weekly_programs': weekly_programs,
        # 唐宋八大家数据
        'tangsong_programs': tangsong_programs,
        'tangsong_programs_count': tangsong_programs_count,
        'tangsong_color': tangsong_color,
        # 大唐诗人传数据
        'tang_poets_programs': tang_poets_programs,
        'tang_poets_programs_count': tang_poets_programs_count,
        'tang_poets_color': tang_poets_color,
        # 学期信息
        'semester_name': config.semester_name,
        'first_week_date': config.first_week_start_date,
    }

    return render(request, 'index.html', context)


def next_program_date(current_date, day_of_week):
    """
    计算下一个指定星期几的日期

    参数:
    current_date: 当前日期
    day_of_week: 目标星期几（1=周一，2=周二，4=周四）

    返回:
    下一个符合条件的日期
    """
    # 调整为Python周日表示（0-6，其中0是周一）
    python_day_of_week = day_of_week - 1  # 转换为Python的星期表示

    days_ahead = python_day_of_week - current_date.weekday()
    if days_ahead <= 0:  # 目标日期已经过去或者就是今天
        days_ahead += 7  # 推迟到下周同一天

    # 特殊处理周二的节目（需要多加一周，即14天后）
    if day_of_week == 2:
        days_ahead += 7  # 再额外增加一周

    next_date = current_date + datetime.timedelta(days=days_ahead)
    return next_date.date()  # 返回日期部分


def program_history(request, category_id):
    """显示某个节目类别的历史节目"""
    category = get_object_or_404(ProgramCategory, id=category_id)
    programs = Program.objects.filter(
        category=category,
        is_active=True  # 只显示活跃的节目
    ).order_by('-publish_date')

    # 获取系统配置
    config = SystemConfig.get_current_config()

    context = {
        'category': category,
        'programs': programs,
        'semester_name': config.semester_name,
    }

    return render(request, 'program_history.html', context)


def video_player(request):
    """
    视频播放页面视图
    """
    # 获取视频URL，2小时有效期
    video_url = get_video_url(expires=72000)

    # 准备视图上下文
    context = {
        'video_url': video_url,
        'video_title': '室内运动视频'
    }

    return render(request, 'video_player.html', context)


def video_player2(request):
    """
    视频播放页面视图
    """
    # 获取视频URL，2小时有效期
    video_url = get_video_url2(expires=72000)

    # 准备视图上下文
    context = {
        'video_url': video_url,
        'video_title': '朝会思政'
    }

    return render(request, 'video_player.html', context)
