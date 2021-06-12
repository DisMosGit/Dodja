from django.conf import settings
from django.views.generic.base import RedirectView
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from note.views import NoteView
from monitoring.views import MonitoringView, MonitoringLogView
from docker_host.views import HostViewSet, AccessViewSet, JobViewSet
from hint.views import HintViewSet
from profile.views import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(
    r'host',
    HostViewSet,
    basename='host',
)
router.register(
    r'host/(?P<host__pk>[^/.]+)/access',
    AccessViewSet,
    basename='access',
)
router.register(
    r'host/(?P<host__pk>[^/.]+)/job',
    JobViewSet,
    basename='job',
)
router.register(
    r'host/(?P<host__pk>[^/.]+)/note',
    NoteView,
    basename='note',
)
router.register(
    r'host/(?P<host__pk>[^/.]+)/monitoring',
    MonitoringView,
    basename='monitoring',
)
router.register(
    r'host/(?P<host__pk>[^/.]+)/monitoring/(?P<monitoring__pk>[^/.]+)/log',
    MonitoringLogView,
    basename='monitoring-log',
)
router.register(
    r'hint',
    HintViewSet,
    basename='hint',
)
router.register(
    r'user',
    UserViewSet,
    basename='user',
)
router.register(
    r'profile',
    ProfileViewSet,
    basename='profile',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/html/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/json/', include('dj_rest_auth.urls')),
    path('api-auth/json/registration/',
         include('dj_rest_auth.registration.urls')),
    # re_path(r'^favicon\.ico$',
    #         RedirectView.as_view(url='static/favicon.ico', permanent=True)),
    # static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
] + static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
