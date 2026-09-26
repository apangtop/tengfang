import datetime
from unittest.mock import Mock, patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .forms import BroadcastCardForm, SystemConfigForm
from .models import BroadcastCard, Program, ProgramCategory, SystemConfig
from .services.cards import build_home_cards
from .services.oss import get_signed_video_url
from .services.schedule import next_program_date, week_number_for


class ScheduleTests(SimpleTestCase):
    def test_week_number_before_and_during_semester(self):
        first_day = datetime.date(2026, 9, 7)
        self.assertEqual(week_number_for(datetime.date(2026, 9, 6), first_day), 0)
        self.assertEqual(week_number_for(first_day, first_day), 1)
        self.assertEqual(week_number_for(datetime.date(2026, 9, 20), first_day), 2)
        self.assertEqual(week_number_for(datetime.date(2026, 9, 21), first_day), 3)

    def test_next_program_date_preserves_tuesday_rotation_rule(self):
        monday = datetime.date(2026, 9, 7)
        self.assertEqual(next_program_date(monday, 1), datetime.date(2026, 9, 14))
        self.assertEqual(next_program_date(monday, 2), datetime.date(2026, 9, 15))
        self.assertEqual(next_program_date(monday, 4), datetime.date(2026, 9, 10))


class AdminFormTests(TestCase):
    def test_semester_must_start_on_monday(self):
        form = SystemConfigForm(
            data={"semester_name": "测试学期", "first_week_start_date": "2026-09-08"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "第一周起始日期必须是星期一", form.errors["first_week_start_date"][0]
        )

    def test_program_card_requires_category(self):
        form = BroadcastCardForm(
            data={
                "title": "节目",
                "card_type": BroadcastCard.TYPE_LATEST_PROGRAM,
                "color": "blue",
                "icon_class": "fa-play",
                "button_text": "播放",
                "sort_order": 10,
                "is_active": True,
                "show_latest_program": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

    def test_direct_link_card_requires_url(self):
        form = BroadcastCardForm(
            data={
                "title": "链接",
                "card_type": BroadcastCard.TYPE_DIRECT_LINK,
                "color": "blue",
                "icon_class": "fa-link",
                "button_text": "打开",
                "sort_order": 10,
                "is_active": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("link_url", form.errors)


class HomeCardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SystemConfig.objects.all().delete()
        SystemConfig.objects.create(
            semester_name="2026年秋季学期",
            first_week_start_date=datetime.date(2026, 9, 7),
        )
        cls.category = ProgramCategory.objects.create(
            name="新闻周刊", day_of_week=1, color="blue"
        )
        cls.program = Program.objects.create(
            category=cls.category,
            title="本周新闻",
            publish_date=datetime.date(2026, 9, 7),
            link="https://example.com/program",
        )

    def setUp(self):
        BroadcastCard.objects.all().delete()
        self.now = datetime.datetime(
            2026, 9, 8, 10, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        )

    def test_legacy_cards_remain_available_before_card_configuration(self):
        cards = build_home_cards(self.now, is_odd_week=True)
        self.assertEqual(cards[0]["subtitle"], "新闻周刊")
        self.assertEqual(cards[0]["action_url"], self.program.link)
        self.assertEqual(
            [card["id"] for card in cards[-2:]], ["video-one", "video-two"]
        )

    def test_configured_latest_program_card_keeps_existing_action(self):
        card = BroadcastCard.objects.create(
            title="周一节目",
            card_type=BroadcastCard.TYPE_LATEST_PROGRAM,
            category=self.category,
            color="blue",
            sort_order=10,
        )
        cards = build_home_cards(self.now, is_odd_week=True)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["id"], card.id)
        self.assertEqual(cards[0]["action_url"], self.program.link)

    def test_all_inactive_cards_do_not_fall_back_to_legacy_cards(self):
        BroadcastCard.objects.create(
            title="已停用",
            card_type=BroadcastCard.TYPE_VIDEO_ONE,
            color="blue",
            is_active=False,
        )
        self.assertEqual(build_home_cards(self.now, is_odd_week=True), [])

    def test_single_and_double_week_cards_alternate(self):
        single = ProgramCategory.objects.create(
            name="今日说法", day_of_week=2, is_biweekly=False
        )
        double = ProgramCategory.objects.create(
            name="世界周刊", day_of_week=2, is_biweekly=True
        )
        for category in (single, double):
            Program.objects.create(
                category=category,
                title=category.name,
                publish_date=datetime.date(2026, 9, 7),
                link="https://example.com/show",
            )
            BroadcastCard.objects.create(
                title=category.name,
                card_type=BroadcastCard.TYPE_LATEST_PROGRAM,
                category=category,
            )

        odd_cards = build_home_cards(self.now, is_odd_week=True)
        even_cards = build_home_cards(self.now, is_odd_week=False)
        self.assertEqual([card["category"] for card in odd_cards], [single])
        self.assertEqual([card["category"] for card in even_cards], [double])


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SystemConfig.objects.all().delete()
        SystemConfig.objects.create(
            semester_name="2026年秋季学期",
            first_week_start_date=datetime.date(2026, 9, 7),
        )
        cls.category = ProgramCategory.objects.create(name="新闻周刊", day_of_week=1)
        cls.active_program = Program.objects.create(
            category=cls.category,
            title="启用节目",
            publish_date=datetime.date(2026, 9, 7),
            link="https://example.com/active",
        )
        Program.objects.create(
            category=cls.category,
            title="停用节目",
            publish_date=datetime.date(2026, 9, 8),
            link="https://example.com/inactive",
            is_active=False,
        )

    def test_home_and_history_routes_are_compatible(self):
        home = self.client.get(reverse("index"))
        history = self.client.get(
            reverse("broadcast:program_history", args=[self.category.pk])
        )
        self.assertEqual(home.status_code, 200)
        self.assertEqual(history.status_code, 200)
        self.assertContains(history, "启用节目")
        self.assertNotContains(history, "停用节目")

    @patch(
        "broadcast.views.get_signed_video_url",
        return_value="https://example.com/signed.mp4",
    )
    def test_video_route_renders_signed_url(self, signer):
        response = self.client.get(reverse("video_player"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://example.com/signed.mp4")
        signer.assert_called_once_with(slot="primary", expires=72000)

    @patch(
        "broadcast.views.get_signed_video_url",
        side_effect=ImproperlyConfigured("missing"),
    )
    def test_missing_video_configuration_has_friendly_error(self, signer):
        response = self.client.get(reverse("video_player2"))
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "视频暂未配置", status_code=503)


class OssServiceTests(SimpleTestCase):
    @override_settings(OSS_VIDEO_PATH_TWO="second.mp4")
    @patch("broadcast.services.oss._build_bucket")
    def test_secondary_video_uses_its_configured_object(self, bucket_builder):
        bucket = Mock()
        bucket.sign_url.return_value = "signed"
        bucket_builder.return_value = bucket
        self.assertEqual(get_signed_video_url("secondary", expires=60), "signed")
        bucket.sign_url.assert_called_once_with("GET", "second.mp4", 60)

    @override_settings(OSS_VIDEO_PATH_TWO="")
    def test_missing_secondary_video_path_is_reported(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "OSS_VIDEO_PATH_TWO"):
            get_signed_video_url("secondary")
