"""Aliyun OSS signed URL generation."""

import oss2
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

VIDEO_PATH_SETTINGS = {
    "primary": "OSS_VIDEO_PATH",
    "secondary": "OSS_VIDEO_PATH_TWO",
}


def _build_bucket():
    required_settings = {
        "OSS_ACCESS_KEY_ID": settings.OSS_ACCESS_KEY_ID,
        "OSS_ACCESS_KEY_SECRET": settings.OSS_ACCESS_KEY_SECRET,
        "OSS_BUCKET_NAME": settings.OSS_BUCKET_NAME,
        "OSS_ENDPOINT": settings.OSS_ENDPOINT,
    }
    missing = [name for name, value in required_settings.items() if not value]
    if missing:
        raise ImproperlyConfigured(f"Missing OSS settings: {', '.join(missing)}")

    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)


def get_signed_video_url(slot="primary", object_key=None, expires=3600):
    try:
        setting_name = VIDEO_PATH_SETTINGS[slot]
    except KeyError as exc:
        raise ValueError(f"Unknown video slot: {slot}") from exc

    object_key = object_key or getattr(settings, setting_name, "")
    if not object_key:
        raise ImproperlyConfigured(f"Missing {setting_name}")
    return _build_bucket().sign_url("GET", object_key, expires)


def get_video_url(object_key=None, expires=3600):
    return get_signed_video_url("primary", object_key, expires)


def get_video_url2(object_key=None, expires=3600):
    return get_signed_video_url("secondary", object_key, expires)
