"""Aliyun OSS signed URL generation."""

import oss2
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError, ProgrammingError

from broadcast.models import OssVideoConfig

VIDEO_PATH_SETTINGS = {
    "primary": "OSS_VIDEO_PATH",
    "secondary": "OSS_VIDEO_PATH_TWO",
}
VIDEO_CONFIG_FIELDS = {
    "primary": "primary_object_key",
    "secondary": "secondary_object_key",
}


def _get_configuration():
    try:
        return OssVideoConfig.objects.first()
    except (OperationalError, ProgrammingError):
        # Keep existing playback available during deployment before migrations.
        return None


def _build_bucket(config=None):
    bucket_name = (config.bucket_name if config else "") or settings.OSS_BUCKET_NAME
    endpoint = (config.endpoint if config else "") or settings.OSS_ENDPOINT
    required_settings = {
        "OSS_ACCESS_KEY_ID": settings.OSS_ACCESS_KEY_ID,
        "OSS_ACCESS_KEY_SECRET": settings.OSS_ACCESS_KEY_SECRET,
        "OSS_BUCKET_NAME": bucket_name,
        "OSS_ENDPOINT": endpoint,
    }
    missing = [name for name, value in required_settings.items() if not value]
    if missing:
        raise ImproperlyConfigured(f"Missing OSS settings: {', '.join(missing)}")

    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, endpoint, bucket_name)


def get_signed_video_url(slot="primary", object_key=None, expires=3600):
    try:
        setting_name = VIDEO_PATH_SETTINGS[slot]
    except KeyError as exc:
        raise ValueError(f"Unknown video slot: {slot}") from exc

    config = _get_configuration()
    configured_key = getattr(config, VIDEO_CONFIG_FIELDS[slot], "")
    object_key = object_key or configured_key or getattr(settings, setting_name, "")
    if not object_key:
        raise ImproperlyConfigured(f"Missing {setting_name}")
    return _build_bucket(config).sign_url("GET", object_key, expires)


def get_video_url(object_key=None, expires=3600):
    return get_signed_video_url("primary", object_key, expires)


def get_video_url2(object_key=None, expires=3600):
    return get_signed_video_url("secondary", object_key, expires)
