import datetime
import re
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
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
    ("purple", "紫色"),
    ("emerald", "绿色"),
    ("green", "绿色（旧）"),
    ("amber", "琥珀"),
    ("yellow", "黄色"),
    ("orange", "橙色"),
    ("pink", "粉色"),
    ("rose", "玫红"),
    ("red", "红色"),
    ("slate", "灰蓝"),
    ("gray", "灰色"),
]


class SystemConfig(models.Model):
    """系统配置"""

    first_week_start_date = models.DateField(
        "第一周起始日期",
        help_text="设置学期第一周的开始日期（周一）",
    )
    semester_name = models.CharField(
        "学期名称", max_length=50, default="2025年春季学期"
    )
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

        config, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "first_week_start_date": first_monday,
                "semester_name": f"{year}年春季学期",
            },
        )
        return config

    @classmethod
    def get_current_week_number(cls):
        from .services.schedule import week_number_for

        config = cls.get_current_config()
        return week_number_for(timezone.localdate(), config.first_week_start_date)

    @classmethod
    def is_odd_week(cls):
        week_number = cls.get_current_week_number()
        return week_number > 0 and week_number % 2 == 1


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

    def save(self, *args, **kwargs):
        self.name = (self.name or "").strip()
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.title = (self.title or "").strip()
        super().save(*args, **kwargs)


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
    color = models.CharField(
        "主题颜色", max_length=20, choices=COLOR_CHOICES, default="blue"
    )
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


class OssVideoConfig(models.Model):
    """Editable media locations; credentials remain in server configuration."""

    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    bucket_name = models.CharField(
        "Bucket 名称",
        max_length=63,
        blank=True,
        help_text="留空沿用服务器的 OSS_BUCKET_NAME。",
    )
    endpoint = models.CharField(
        "Endpoint",
        max_length=255,
        blank=True,
        help_text="例如 https://oss-cn-chengdu.aliyuncs.com；留空沿用服务器配置。",
    )
    primary_object_key = models.CharField(
        "室内运动视频路径",
        max_length=1024,
        blank=True,
        help_text="填写 Bucket 内的对象路径，例如 videos/exercise.mp4。留空沿用原配置。",
    )
    secondary_object_key = models.CharField(
        "朝会思政视频路径",
        max_length=1024,
        blank=True,
        help_text="填写 Bucket 内的对象路径，例如 videos/morning.mp4。留空沿用原配置。",
    )
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "OSS 视频配置"
        verbose_name_plural = "OSS 视频配置"

    def __str__(self):
        return "校园视频 OSS 配置"

    def clean(self):
        super().clean()
        self.bucket_name = self.bucket_name.strip()
        self.endpoint = self.endpoint.strip()
        errors = {}
        if self.bucket_name and not re.match(
            r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", self.bucket_name
        ):
            errors["bucket_name"] = (
                "Bucket 名称须为 3–63 位小写字母、数字或连字符，首尾不能是连字符。"
            )
        if self.endpoint:
            if "://" not in self.endpoint:
                self.endpoint = "https://" + self.endpoint
            try:
                parsed = urlsplit(self.endpoint)
                valid = (
                    parsed.scheme in ("http", "https")
                    and parsed.hostname
                    and not parsed.username
                    and not parsed.password
                    and parsed.path in ("", "/")
                    and not parsed.query
                    and not parsed.fragment
                    and not any(c.isspace() for c in self.endpoint)
                )
                valid = valid and (parsed.port is None or parsed.port > 0)
            except ValueError:
                valid = False
            if not valid:
                errors["endpoint"] = (
                    "请填写 OSS Endpoint 域名，不要填写视频完整链接、账号或路径。"
                )
            else:
                self.endpoint = self.endpoint.rstrip("/")
        for field in ("primary_object_key", "secondary_object_key"):
            value = getattr(self, field).strip()
            setattr(self, field, value)
            if value.startswith(("/", "http://", "https://")):
                errors[field] = (
                    "请填写 Bucket 内的对象路径，不要填写完整 URL 或以 / 开头。"
                )
        if errors:
            raise ValidationError(errors)
