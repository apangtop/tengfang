import oss2
from Tfang_school import settings


def get_video_url(object_key=None, expires=3600):
    # 配置OSS认证信息
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)

    # 如果没有提供object_key，使用默认设置
    if object_key is None:
        object_key = settings.OSS_VIDEO_PATH

    # 确保路径编码正确，特别是对于包含中文的路径
    from urllib.parse import quote
    encoded_object_key = quote(object_key)

    # 打印路径用于调试
    print(f"原始路径: {object_key}")
    print(f"编码后路径: {encoded_object_key}")

    # 生成带签名的URL，有效期为指定秒数
    url = bucket.sign_url('GET', object_key, expires)
    return url


def get_video_url2(object_key=None, expires=3600):
    # 配置OSS认证信息
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)

    # 如果没有提供object_key，使用默认设置
    if object_key is None:
        object_key = settings.OSS_VIDEO_PATH_three

    # 确保路径编码正确，特别是对于包含中文的路径
    from urllib.parse import quote
    encoded_object_key = quote(object_key)

    # 打印路径用于调试
    print(f"原始路径: {object_key}")
    print(f"编码后路径: {encoded_object_key}")

    # 生成带签名的URL，有效期为指定秒数
    url = bucket.sign_url('GET', object_key, expires)
    return url
