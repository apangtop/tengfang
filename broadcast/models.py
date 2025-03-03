from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime


class SystemConfig(models.Model):
    """系统配置"""
    first_week_start_date = models.DateField('第一周起始日期', help_text='设置学期第一周的开始日期（周一）')
    semester_name = models.CharField('学期名称', max_length=50, default='2025年春季学期')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

    def __str__(self):
        return f"{self.semester_name} - 起始日期: {self.first_week_start_date}"

    @classmethod
    def get_current_config(cls):
        """获取当前配置，如果不存在则创建默认配置"""
        config = cls.objects.first()
        if not config:
            # 默认使用当年1月1日后的第一个周一作为起始日期
            year = timezone.now().year
            jan_first = datetime.date(year, 1, 1)
            days_to_monday = (7 - jan_first.weekday()) % 7
            if days_to_monday == 0:
                days_to_monday = 7  # 如果1月1日就是周一，则使用这一天
            first_monday = jan_first + datetime.timedelta(days=days_to_monday)

            config = cls.objects.create(
                first_week_start_date=first_monday,
                semester_name=f"{year}年春季学期"
            )
        return config

    @classmethod
    def get_current_week_number(cls):
        """计算当前是第几周"""
        config = cls.get_current_config()
        today = timezone.now().date()
        first_day = config.first_week_start_date

        # 如果今天在起始日期之前，返回0（学期未开始）
        if today < first_day:
            return 0

        days_diff = (today - first_day).days
        week_number = (days_diff // 7) + 1
        return week_number

    @classmethod
    def is_odd_week(cls):
        """判断当前是否为单周"""
        week_number = cls.get_current_week_number()
        return week_number % 2 == 1


class ProgramCategory(models.Model):
    """节目类别"""
    name = models.CharField('节目名称', max_length=50)
    description = models.TextField('描述', blank=True)
    day_of_week = models.IntegerField('播出星期',
                                      choices=[(1, '周一'), (2, '周二'), (4, '周四')])
    icon_class = models.CharField('图标类名', max_length=50, default='fa-newspaper')
    color = models.CharField('主题颜色', max_length=20, default='blue')
    is_biweekly = models.BooleanField('是否双周轮播', default=False)
    alternate_with = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='alternate_program',
                                       verbose_name='轮替节目')

    class Meta:
        verbose_name = '节目类别'
        verbose_name_plural = '节目类别'
        ordering = ['day_of_week']

    def __str__(self):
        return self.name

    def is_odd_week(self):
        """判断当前是否为单周"""
        return SystemConfig.is_odd_week()

    def should_display(self):
        """判断在当前周是否应该显示该节目"""
        if not self.is_biweekly:
            return True

        # 对于双周轮播节目，需要根据单双周来确定是否显示
        is_odd = self.is_odd_week()
        # 假设单周显示主节目，双周显示轮替节目
        if is_odd and not self.alternate_with:
            return True
        elif not is_odd and self.alternate_with:
            return False
        return False


class Program(models.Model):
    """具体节目"""
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE,
                                 related_name='programs', verbose_name='节目类别')
    title = models.CharField('标题', max_length=100)
    publish_date = models.DateField('发布日期')
    link = models.URLField('节目链接')
    is_active = models.BooleanField('当前活跃', default=True)

    class Meta:
        verbose_name = '节目'
        verbose_name_plural = '节目'
        ordering = ['-publish_date']

    def __str__(self):
        return self.title