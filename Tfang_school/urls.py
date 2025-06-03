from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from broadcast.views import index, video_player, video_player2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include('broadcast.urls.broadcast_urls')),
    path('video/', video_player, name='video_player'),
    path('video2/', video_player2, name='video_player2'),
    path('qrcode_upload/', include('qrcode_upload.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

