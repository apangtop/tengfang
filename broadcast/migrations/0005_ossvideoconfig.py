from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("broadcast", "0004_sync_model_state")]

    operations = [
        migrations.CreateModel(
            name="OssVideoConfig",
            fields=[
                ("id", models.PositiveSmallIntegerField(default=1, editable=False, primary_key=True, serialize=False)),
                ("bucket_name", models.CharField(blank=True, help_text="留空沿用服务器的 OSS_BUCKET_NAME。", max_length=63, verbose_name="Bucket 名称")),
                ("endpoint", models.CharField(blank=True, help_text="例如 https://oss-cn-chengdu.aliyuncs.com；留空沿用服务器配置。", max_length=255, verbose_name="Endpoint")),
                ("primary_object_key", models.CharField(blank=True, help_text="填写 Bucket 内的对象路径，例如 videos/exercise.mp4。留空沿用原配置。", max_length=1024, verbose_name="室内运动视频路径")),
                ("secondary_object_key", models.CharField(blank=True, help_text="填写 Bucket 内的对象路径，例如 videos/morning.mp4。留空沿用原配置。", max_length=1024, verbose_name="朝会思政视频路径")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
            ],
            options={"verbose_name": "OSS 视频配置", "verbose_name_plural": "OSS 视频配置"},
        ),
    ]
