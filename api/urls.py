from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'collections', views.CollectionsViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('status/', views.check_status, name='status'),
    path('metrics/', views.metrics, name='metrics'),
    path('version/', views.version, name='version'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
