from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .admin import settings

urlpatterns = [
    path('', views.index),
    path('settings', settings),
    path("dashboard/", cache_page(300)(views.dashboard), name='dashboard'),
    path(r'dashboard/direction/', views.windDirection, name="windDirection"),
    path(r'dashboard/info', views.infoPage, name="info", ),
    path('dashboard/download', views.download_page, name='download'),
    path('dashboard/download/file', views.download_file_page, name='downloadFile'),
    path('dashboard/download/mirror/file', views.file, name='fileMirror'),
]
