from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('file/<str:filename>/', views.get_file, name='get_file'),
] 