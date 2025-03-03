# broadcast/urls/broadcast_urls.py
from django.urls import path
from broadcast.views import program_history

app_name = 'broadcast'

urlpatterns = [
    path('history/<int:category_id>/', program_history, name='program_history'),
]