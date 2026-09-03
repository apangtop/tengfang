from django.db import migrations


SPECIAL_NAMES = {"唐宋八大家", "大唐诗人传"}


def seed_cards(apps, schema_editor):
    BroadcastCard = apps.get_model("broadcast", "BroadcastCard")
    ProgramCategory = apps.get_model("broadcast", "ProgramCategory")

    if BroadcastCard.objects.exists():
        return

    order = 10
    for category in ProgramCategory.objects.all().order_by("day_of_week", "id"):
        is_special = category.name in SPECIAL_NAMES
        BroadcastCard.objects.create(
            title="晚读经典赏析" if is_special else dict(category._meta.get_field("day_of_week").choices).get(category.day_of_week, "节目"),
            subtitle=category.name,
            description=category.description or "",
            icon_class=category.icon_class or ("fa-book-open" if is_special else "fa-newspaper"),
            color=category.color if category.color in {"blue", "indigo", "emerald", "amber", "rose", "slate"} else "blue",
            card_type="program_list" if is_special else "latest_program",
            category=category,
            button_text="浏览所有节目" if is_special else "播放本周节目",
            show_latest_program=not is_special,
            sort_order=order,
        )
        order += 10

    BroadcastCard.objects.create(
        title="课间操视频",
        subtitle="室内课间操",
        description="固定视频入口",
        icon_class="fa-chalkboard-teacher",
        color="blue",
        card_type="video_one",
        button_text="播放视频",
        show_latest_program=False,
        sort_order=order,
    )
    BroadcastCard.objects.create(
        title="朝会思政",
        subtitle="思想政治教育",
        description="固定视频入口",
        icon_class="fa-flag",
        color="rose",
        card_type="video_two",
        button_text="播放本周节目",
        show_latest_program=False,
        sort_order=order + 10,
    )


def unseed_cards(apps, schema_editor):
    BroadcastCard = apps.get_model("broadcast", "BroadcastCard")
    BroadcastCard.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("broadcast", "0002_broadcastcard"),
    ]

    operations = [
        migrations.RunPython(seed_cards, unseed_cards),
    ]
