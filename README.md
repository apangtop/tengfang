# 腾声汇

腾芳中学校园广播节目平台。后台维护学期、节目类别、节目和首页卡片，前台按当前周次显示节目并提供视频入口。

## 本地运行

要求 Python 3.10–3.14，推荐使用 Python 3.12。

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
