from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.index),
    path("dashboard/", cache_page(300)(views.dashboard), name='dashboard'),
    path(r'dashboard/direction/', views.windDirection, name="windDirection"),
    path(r'dashboard/info', views.infoPage, name="info",)
]
