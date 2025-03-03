from django.contrib import admin
from django.urls import path, include

from broadcast.views import index, video_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include('broadcast.urls.broadcast_urls')),
    path('video/', video_player, name='video_player'),
]

