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

## Recommended next steps

1. Rotate the Aliyun OSS AccessKey that was previously committed in `settings.py`.
2. Create a real `.env` from `.env.example` on the server and keep it out of git.
3. Fix the garbled template/source encoding by converting all project text files to UTF-8.
4. Upgrade the runtime from Python 3.6 to a supported Python version, then move Django from 3.2 LTS to a current LTS release.
5. Replace `broadcast/oos_helper.py` with a service module named `oss_helper.py`, then update imports. The current filename has a typo but was preserved to keep the change small.
6. Move display rules for weekly, biweekly, and special programs into model/query service functions so `broadcast/views.py` only prepares view context.
7. Add tests for week-number calculation, biweekly filtering, and video URL configuration failures.
8. Rebuild deployment around a reproducible environment instead of committing or copying `venv/`, `staticfiles/`, logs, SQL dumps, and server artifacts.

## Bigger cleanup idea

This project is small enough that a conservative Django app is still a good fit. The strange parts are mostly operational drift: copied Linux virtualenv, committed static output, SQL dump, hard-coded credentials, mixed encodings, and view logic that has grown around one page.

Keep Django, but make the app boring:

- `broadcast/models.py`: database shape only plus small domain methods.
- `broadcast/services/schedule.py`: week and program selection.
- `broadcast/services/oss.py`: signed media URLs.
- `broadcast/views.py`: request handling and template context.
- `templates/`: UTF-8 templates with repeated card markup extracted into includes.
- `.env`: deployment-specific configuration only.
