from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("broadcast", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BroadcastCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=80, verbose_name="卡片标题")),
                ("subtitle", models.CharField(blank=True, max_length=120, verbose_name="副标题")),
                ("description", models.TextField(blank=True, verbose_name="说明")),
                ("icon_class", models.CharField(default="fa-play", max_length=50, verbose_name="图标类名")),
                ("color", models.CharField(choices=[("blue", "蓝色"), ("indigo", "靛蓝"), ("emerald", "绿色"), ("amber", "琥珀"), ("rose", "玫红"), ("slate", "灰蓝")], default="blue", max_length=20, verbose_name="主题颜色")),
                ("card_type", models.CharField(choices=[("latest_program", "最新节目卡片"), ("program_list", "节目列表卡片"), ("direct_link", "外部链接卡片"), ("video_one", "室内运动视频"), ("video_two", "朝会思政视频")], max_length=30, verbose_name="卡片类型")),
                ("link_url", models.URLField(blank=True, verbose_name="外部链接")),
                ("button_text", models.CharField(default="立即播放", max_length=40, verbose_name="按钮文字")),
                ("show_latest_program", models.BooleanField(default=True, verbose_name="显示最新节目日期")),
                ("is_active", models.BooleanField(default=True, verbose_name="启用")),
                ("sort_order", models.PositiveIntegerField(default=100, verbose_name="排序")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="cards", to="broadcast.programcategory", verbose_name="关联节目类别")),
            ],
            options={
                "verbose_name": "首页卡片",
                "verbose_name_plural": "首页卡片",
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
