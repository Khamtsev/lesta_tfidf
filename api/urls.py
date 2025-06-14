from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="TF-IDF API",
        default_version='v1',
        description="API для работы с TF-IDF",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'collections', views.CollectionViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

    path('status/', views.check_status, name='status'),
    path('metrics/', views.metrics, name='metrics'),
    path('version/', views.version, name='version'),
    path('collections/<int:pk>/statistics/',
         views.CollectionViewSet.as_view({'get': 'get_collection_statistics'}),
         name='collection-statistics'),
    path('collections/<int:pk>/<int:document_id>/',
         views.CollectionViewSet.as_view({
             'post': 'create_document',
             'delete': 'destroy_document'
         }),
         name='collection-document'),
    path('documents/<int:pk>/statistics/',
         views.DocumentViewSet.as_view({'get': 'get_document_statistics'}),
         name='document-statistics'),
    path('documents/<int:pk>/huffman/',
         views.DocumentViewSet.as_view({'get': 'get_huffman'}),
         name='document-huffman'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
