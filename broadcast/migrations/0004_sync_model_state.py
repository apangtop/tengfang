from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("broadcast", "0003_seed_broadcast_cards")]

    operations = [
        migrations.AlterModelOptions(
            name="programcategory",
            options={
                "ordering": ["day_of_week", "name"],
                "verbose_name": "节目类别",
                "verbose_name_plural": "节目类别",
            },
        ),
        migrations.AlterField(
            model_name="broadcastcard",
            name="color",
            field=models.CharField(
                choices=[
                    ("blue", "蓝色"), ("indigo", "靛蓝"), ("purple", "紫色"),
                    ("emerald", "绿色"), ("green", "绿色（旧）"), ("amber", "琥珀"),
                    ("yellow", "黄色"), ("orange", "橙色"), ("pink", "粉色"),
                    ("rose", "玫红"), ("red", "红色"), ("slate", "灰蓝"),
                    ("gray", "灰色"),
                ],
                default="blue",
                max_length=20,
                verbose_name="主题颜色",
            ),
        ),
        migrations.AlterField(
            model_name="programcategory",
            name="day_of_week",
            field=models.IntegerField(
                choices=[(1, "周一"), (2, "周二"), (3, "周三"), (4, "周四"), (5, "周五")],
                verbose_name="播出星期",
            ),
        ),
    ]
