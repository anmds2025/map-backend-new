# map/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from map.views.auth import login, register, logout
from map.views.hazard_report import HazardReportViewSet

router = DefaultRouter()
router.register(r'reports', HazardReportViewSet, basename='hazardreport')

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('', include(router.urls)),   # gắn tất cả CRUD endpoint cho HazardReport
]
