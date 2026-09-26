# 腾声汇

腾芳中学校园广播节目平台。后台维护学期、节目类别、节目和首页卡片，前台按当前周次显示节目并提供视频入口。

## 本地运行

原有 Python 3.6 / Django 3.2 服务器可继续使用；依赖文件按 Python 版本选择原有依赖或现代依赖。新建环境推荐使用 Python 3.12。服务器运行环境升级应单独安排。

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

本地调试可在 `.env` 中使用 SQLite：

```dotenv
DEBUG=true
DB_ENGINE=sqlite
SQLITE_PATH=db.sqlite3
SESSION_COOKIE_SECURE=false
CSRF_COOKIE_SECURE=false
```

然后初始化并启动：

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 生产配置

生产环境必须在 `.env` 中配置 `SECRET_KEY`、数据库和 OSS 凭据。两个固定视频分别使用 `OSS_VIDEO_PATH` 与 `OSS_VIDEO_PATH_TWO`。部署前执行：

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
gunicorn -c gunicorn_config.py Tfang_school.wsgi:application
```

## 后台修改 OSS 视频

执行迁移后，在 `/admin/` 的 Broadcast 分组进入「OSS 视频配置」，首次点击「添加」。

- Bucket 名称与 Endpoint 可修改，留空使用服务器原有配置。
- 「室内运动视频路径」对应 `/video/`，「朝会思政视频路径」对应 `/video2/`。
- 对象路径填写 `videos/example.mp4` 这样的 Bucket 内路径，不填写完整 URL 或临时签名链接。
- 保存后下一次打开或刷新视频页面立即使用新配置，无需重启服务；已打开的视频页面需要刷新。
- AccessKey ID / Secret 仍来自服务器原有环境变量，不写入该数据库表，也不显示在后台。
- 未添加配置、字段留空时均沿用原配置。后台只保留一份配置，支持修改，不提供删除入口。

上线时使用现有服务器解释器，代码上传后执行：

```bash
cd /var/www/tengfang
/root/venv/bin/python3 manage.py check
/root/venv/bin/python3 manage.py migrate
systemctl restart django-tengfang.service
```

## 测试

测试使用临时 SQLite 数据库，不会访问生产数据库或 OSS：

```powershell
$env:DB_ENGINE="sqlite"
$env:SECRET_KEY="test-only"
python manage.py test
```

## 兼容说明

- 原有 `/`、`/admin/`、`/api/history/<id>/`、`/video/`、`/video2/` 地址保持不变。
- `broadcast.oos_helper` 仍可导入，实际实现已迁移到 `broadcast.services.oss`。
- 数据库尚未创建首页卡片时仍展示旧版默认卡片；如果已有卡片但全部停用，首页会正确显示“暂无卡片”。
