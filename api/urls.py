from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('status/', views.status, name='status'),
    path('metrics/', views.metrics, name='metrics'),
    path('version/', views.version, name='version'),
]
