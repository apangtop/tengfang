from django.contrib import admin

from .forms import ProgramCategoryForm, ProgramForm
from .models import BroadcastCard, Program, ProgramCategory, SystemConfig


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ("semester_name", "first_week_start_date", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        if SystemConfig.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class ProgramInline(admin.TabularInline):
    model = Program
    form = ProgramForm
    extra = 1
    fields = ("title", "publish_date", "link", "is_active")


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    form = ProgramCategoryForm
    list_display = ("name", "day_of_week", "is_biweekly", "alternate_with", "color")
    list_filter = ("day_of_week", "is_biweekly", "color")
    search_fields = ("name", "description")
    inlines = [ProgramInline]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramForm
    list_display = ("title", "category", "publish_date", "is_active")
    list_filter = ("category", "publish_date", "is_active")
    search_fields = ("title", "category__name")
    date_hierarchy = "publish_date"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category").order_by("-publish_date")


@admin.register(BroadcastCard)
class BroadcastCardAdmin(admin.ModelAdmin):
    list_display = ("title", "card_type", "category", "sort_order", "is_active", "updated_at")
    list_editable = ("sort_order", "is_active")
    list_filter = ("card_type", "color", "is_active")
    search_fields = ("title", "subtitle", "description", "category__name")
    autocomplete_fields = ("category",)
    fieldsets = (
        ("展示内容", {
            "fields": ("title", "subtitle", "description", "icon_class", "color", "button_text")
        }),
        ("行为", {
            "fields": ("card_type", "category", "link_url", "show_latest_program")
        }),
        ("发布", {
            "fields": ("sort_order", "is_active")
        }),
    )
