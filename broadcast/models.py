import datetime

from django.db import models
from django.utils import timezone


DAY_CHOICES = [
    (1, "周一"),
    (2, "周二"),
    (3, "周三"),
    (4, "周四"),
    (5, "周五"),
]

COLOR_CHOICES = [
    ("blue", "蓝色"),
    ("indigo", "靛蓝"),
    ("emerald", "绿色"),
    ("amber", "琥珀"),
    ("rose", "玫红"),
    ("slate", "灰蓝"),
]


class SystemConfig(models.Model):
    """系统配置"""

    first_week_start_date = models.DateField(
        "第一周起始日期",
        help_text="设置学期第一周的开始日期（周一）",
    )
    semester_name = models.CharField("学期名称", max_length=50, default="2025年春季学期")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "系统配置"
        verbose_name_plural = "系统配置"

    def __str__(self):
        return f"{self.semester_name} - 起始日期: {self.first_week_start_date}"

    @classmethod
    def get_current_config(cls):
        config = cls.objects.first()
        if config:
            return config

        year = timezone.now().year
        jan_first = datetime.date(year, 1, 1)
        days_to_monday = (7 - jan_first.weekday()) % 7
        first_monday = jan_first + datetime.timedelta(days=days_to_monday)

        return cls.objects.create(
            first_week_start_date=first_monday,
            semester_name=f"{year}年春季学期",
        )

    @classmethod
    def get_current_week_number(cls):
        config = cls.get_current_config()
        today = timezone.now().date()
        first_day = config.first_week_start_date

        if today < first_day:
            return 0

        return ((today - first_day).days // 7) + 1

    @classmethod
    def is_odd_week(cls):
        return cls.get_current_week_number() % 2 == 1


class ProgramCategory(models.Model):
    """节目类别"""

    name = models.CharField("节目名称", max_length=50)
    description = models.TextField("描述", blank=True)
    day_of_week = models.IntegerField("播出星期", choices=DAY_CHOICES)
    icon_class = models.CharField("图标类名", max_length=50, default="fa-newspaper")
    color = models.CharField("主题颜色", max_length=20, default="blue")
    is_biweekly = models.BooleanField("是否双周轮播", default=False)
    alternate_with = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alternate_program",
        verbose_name="轮替节目",
    )

    class Meta:
        verbose_name = "节目类别"
        verbose_name_plural = "节目类别"
        ordering = ["day_of_week", "name"]

    def __str__(self):
        return self.name

    def current_week_label(self):
        if self.day_of_week not in [2, 4]:
            return ""
        return "双周" if self.is_biweekly else "单周"


class Program(models.Model):
    """具体节目"""

    category = models.ForeignKey(
        ProgramCategory,
        on_delete=models.CASCADE,
        related_name="programs",
        verbose_name="节目类别",
    )
    title = models.CharField("标题", max_length=100)
    publish_date = models.DateField("发布日期")
    link = models.URLField("节目链接")
    is_active = models.BooleanField("当前活跃", default=True)

    class Meta:
        verbose_name = "节目"
        verbose_name_plural = "节目"
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title


class BroadcastCard(models.Model):
    """首页卡片"""

    TYPE_LATEST_PROGRAM = "latest_program"
    TYPE_PROGRAM_LIST = "program_list"
    TYPE_DIRECT_LINK = "direct_link"
    TYPE_VIDEO_ONE = "video_one"
    TYPE_VIDEO_TWO = "video_two"

    CARD_TYPE_CHOICES = [
        (TYPE_LATEST_PROGRAM, "最新节目卡片"),
        (TYPE_PROGRAM_LIST, "节目列表卡片"),
        (TYPE_DIRECT_LINK, "外部链接卡片"),
        (TYPE_VIDEO_ONE, "室内运动视频"),
        (TYPE_VIDEO_TWO, "朝会思政视频"),
    ]

    title = models.CharField("卡片标题", max_length=80)
    subtitle = models.CharField("副标题", max_length=120, blank=True)
    description = models.TextField("说明", blank=True)
    icon_class = models.CharField("图标类名", max_length=50, default="fa-play")
    color = models.CharField("主题颜色", max_length=20, choices=COLOR_CHOICES, default="blue")
    card_type = models.CharField("卡片类型", max_length=30, choices=CARD_TYPE_CHOICES)
    category = models.ForeignKey(
        ProgramCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cards",
        verbose_name="关联节目类别",
    )
    link_url = models.URLField("外部链接", blank=True)
    button_text = models.CharField("按钮文字", max_length=40, default="立即播放")
    show_latest_program = models.BooleanField("显示最新节目日期", default=True)
    is_active = models.BooleanField("启用", default=True)
    sort_order = models.PositiveIntegerField("排序", default=100)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "首页卡片"
        verbose_name_plural = "首页卡片"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title
