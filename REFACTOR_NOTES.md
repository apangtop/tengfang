# Refactor Notes

## Immediate security work already started

- Removed the `qrcode_upload` Django app and its `/qrcode_upload/` routes.
- Moved Django and OSS secrets to environment variables.
- Changed production defaults so `DEBUG` is off unless explicitly enabled.
- Replaced open CORS defaults with an allow-list.
- Added missing runtime dependencies for `django-cors-headers` and `oss2`.
- Refactored the homepage to render configurable `BroadcastCard` records.

## How to add homepage cards

1. Run migrations so the `首页卡片` table exists.
2. Open Django admin and add a `首页卡片`.
3. Choose a card type:
   - `最新节目卡片`: link to the latest active program in a selected category.
   - `节目列表卡片`: open a modal list for all active programs in a selected category.
   - `外部链接卡片`: open a manually configured URL.
   - `室内运动视频` / `朝会思政视频`: use the existing built-in video player routes.
4. Use `排序` to control homepage order and `启用` to hide/show cards.

## Completed in the compatibility refactor

1. Upgraded the supported runtime target to Python 3.10–3.14 and Django 5.2 LTS.
2. Moved semester scheduling, program selection, homepage cards, and OSS signing into focused services.
3. Kept `broadcast/oos_helper.py` as a compatibility import while using `broadcast/services/oss.py` internally.
4. Added regression coverage for week calculation, biweekly filtering, card fallback, admin validation, routes, history, and video configuration failures.
5. Added the missing model-state migration and reproducible local/production setup documentation.
6. Made file logging optional and rotating, and made HTTPS/HSTS deployment settings configurable.

## Remaining operational work

1. Rotate the Aliyun OSS AccessKey that was previously committed in `settings.py`.
2. Create a real `.env` from `.env.example` on the server and keep it out of git.
3. Stop distributing the historical committed `venv/`, `staticfiles/`, logs, SQL dumps, and server artifacts after confirming the deployment no longer consumes them.
4. Back up the production database, run `python manage.py migrate`, and perform a browser smoke test before switching traffic.

## Bigger cleanup idea

This project is small enough that a conservative Django app is still a good fit. The strange parts are mostly operational drift: copied Linux virtualenv, committed static output, SQL dump, hard-coded credentials, mixed encodings, and view logic that has grown around one page.

Keep Django, but make the app boring:

- `broadcast/models.py`: database shape only plus small domain methods.
- `broadcast/services/schedule.py`: week and program selection.
- `broadcast/services/oss.py`: signed media URLs.
- `broadcast/views.py`: request handling and template context.
- `templates/`: UTF-8 templates with repeated card markup extracted into includes.
- `.env`: deployment-specific configuration only.
