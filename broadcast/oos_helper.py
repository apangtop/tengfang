from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import oss2


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


def get_video_url(object_key=None, expires=3600):
    object_key = object_key or settings.OSS_VIDEO_PATH
    return _build_bucket().sign_url("GET", object_key, expires)


def get_video_url2(object_key=None, expires=3600):
    object_key = object_key or settings.OSS_VIDEO_PATH_TWO
    if not object_key:
        raise ImproperlyConfigured("Missing OSS_VIDEO_PATH_TWO")
    return _build_bucket().sign_url("GET", object_key, expires)
