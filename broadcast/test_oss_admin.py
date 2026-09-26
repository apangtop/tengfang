from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.db.utils import ProgrammingError
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import OssVideoConfig
from .services.oss import get_signed_video_url


@override_settings(
    OSS_VIDEO_PATH="old-exercise.mp4",
    OSS_VIDEO_PATH_TWO="old-morning.mp4",
    OSS_ACCESS_KEY_ID="test-id",
    OSS_ACCESS_KEY_SECRET="test-secret",
    OSS_BUCKET_NAME="old-bucket",
    OSS_ENDPOINT="https://oss-cn-chengdu.aliyuncs.com",
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    },
)
class OssAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            "oss-admin", "admin@example.invalid", "test-password"
        )
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.user)
        self.add_url = reverse("admin:broadcast_ossvideoconfig_add")

    def post_form(self, url, data):
        self.assertEqual(self.client.get(url).status_code, 200)
        token = self.client.cookies["csrftoken"].value
        return self.client.post(
            url, dict(data, csrfmiddlewaretoken=token, _save="Save")
        )

    def payload(self, primary="exercise-new.mp4", secondary="morning-new.mp4"):
        return {
            "bucket_name": "school-videos",
            "endpoint": "oss-cn-chengdu.aliyuncs.com",
            "primary_object_key": primary,
            "secondary_object_key": secondary,
        }

    @patch("broadcast.services.oss._build_bucket")
    def test_admin_add_and_edit_immediately_change_both_video_routes(
        self, bucket_builder
    ):
        bucket = Mock()
        bucket.sign_url.return_value = "https://example.invalid/signed.mp4"
        bucket_builder.return_value = bucket
        added = self.post_form(self.add_url, self.payload())
        self.assertEqual(added.status_code, 302)
        config = OssVideoConfig.objects.get(pk=1)
        self.assertEqual(config.endpoint, "https://oss-cn-chengdu.aliyuncs.com")
        for route, key in (
            ("video_player", "exercise-new.mp4"),
            ("video_player2", "morning-new.mp4"),
        ):
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)
            bucket.sign_url.assert_called_with("GET", key, 72000)
        change_url = reverse("admin:broadcast_ossvideoconfig_change", args=[config.pk])
        self.assertEqual(
            self.post_form(
                change_url, self.payload("exercise-edited.mp4", "morning-edited.mp4")
            ).status_code,
            302,
        )
        for route, key in (
            ("video_player", "exercise-edited.mp4"),
            ("video_player2", "morning-edited.mp4"),
        ):
            self.assertEqual(self.client.get(reverse(route)).status_code, 200)
            bucket.sign_url.assert_called_with("GET", key, 72000)

    def test_connection_overrides_are_used_for_local_signature(self):
        OssVideoConfig.objects.create(**self.payload())
        with (
            patch("broadcast.services.oss.oss2.Auth") as auth,
            patch("broadcast.services.oss.oss2.Bucket") as constructor,
        ):
            get_signed_video_url("primary")
            auth.assert_called_once_with("test-id", "test-secret")
            constructor.assert_called_once_with(
                auth.return_value, "oss-cn-chengdu.aliyuncs.com", "school-videos"
            )

    @patch("broadcast.services.oss._build_bucket")
    def test_original_settings_work_without_admin_configuration(self, builder):
        get_signed_video_url("primary")
        builder.return_value.sign_url.assert_called_with(
            "GET", "old-exercise.mp4", 3600
        )
        get_signed_video_url("secondary")
        builder.return_value.sign_url.assert_called_with("GET", "old-morning.mp4", 3600)

    @patch("broadcast.services.oss._build_bucket")
    def test_blank_paths_fall_back_and_explicit_object_key_takes_priority(
        self, builder
    ):
        OssVideoConfig.objects.create()
        get_signed_video_url("primary")
        builder.return_value.sign_url.assert_called_with(
            "GET", "old-exercise.mp4", 3600
        )
        get_signed_video_url("secondary", object_key="explicit.mp4")
        builder.return_value.sign_url.assert_called_with("GET", "explicit.mp4", 3600)

    @patch("broadcast.services.oss._build_bucket")
    @patch(
        "broadcast.services.oss.OssVideoConfig.objects.first",
        side_effect=ProgrammingError("table missing"),
    )
    def test_playback_falls_back_before_new_migration(self, query, builder):
        get_signed_video_url("primary")
        builder.return_value.sign_url.assert_called_once_with(
            "GET", "old-exercise.mp4", 3600
        )

    def test_invalid_locations_rejected_by_admin(self):
        for field, value in (
            ("bucket_name", "Invalid_Bucket"),
            ("endpoint", "https://oss.example.invalid/video.mp4"),
            ("primary_object_key", "https://example.invalid/video.mp4"),
        ):
            with self.subTest(field=field):
                data = self.payload()
                data[field] = value
                response = self.post_form(self.add_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context["adminform"].form.errors)
                self.assertEqual(OssVideoConfig.objects.count(), 0)

    def test_only_one_configuration_and_no_admin_delete(self):
        self.assertEqual(self.post_form(self.add_url, self.payload()).status_code, 302)
        self.assertEqual(self.client.get(self.add_url).status_code, 403)
        deletion = reverse("admin:broadcast_ossvideoconfig_delete", args=[1])
        self.assertEqual(self.client.get(deletion).status_code, 403)
        self.assertEqual(OssVideoConfig.objects.count(), 1)

    def test_anonymous_users_cannot_change_configuration(self):
        response = Client().post(self.add_url, self.payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OssVideoConfig.objects.count(), 0)

    def test_form_does_not_expose_access_keys(self):
        response = self.client.get(self.add_url)
        self.assertNotContains(response, "test-secret")
        self.assertNotContains(response, "test-id")
