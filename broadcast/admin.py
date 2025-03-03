from django.contrib import admin
from .models import ProgramCategory, Program, SystemConfig


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('semester_name', 'first_week_start_date', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # 只允许创建一个系统配置
        if SystemConfig.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # 不允许删除系统配置
        return False


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_of_week', 'is_biweekly', 'alternate_with')
    list_filter = ('day_of_week', 'is_biweekly')
    search_fields = ('name', 'description')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'is_active')
    list_filter = ('category', 'publish_date', 'is_active')
    search_fields = ('title',)
    date_hierarchy = 'publish_date'

    def get_queryset(self, request):
        """返回最近的100个节目"""
        qs = super().get_queryset(request)
        return qs.order_by('-publish_date')