from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import Metrics, Collections, Document
from core.constants import VERSION
from .serializers import (
    CollectionsCreateSerializer,
    CollectionsSerializer,
    DocumentListSerializer,
    DocumentDetailSerializer,
    DocumentCreateSerializer
)
from users.permissions import IsOwner


@api_view(['GET'])
def check_status(request):
    return Response({"status": "OK"})


@api_view(['GET'])
def metrics(request):
    metrics = Metrics.objects.first()
    if not metrics:
        return Response({
            "files_processed": 0,
            "min_time_processed": 0.0,
            "avg_time_processed": 0.0,
            "max_time_processed": 0.0,
            "latest_file_processed_timestamp": None,
            "avg_file_size": 0.0
        })

    return Response({
        "files_processed": metrics.files_processed,
        "min_time_processed": metrics.min_time_processed,
        "avg_time_processed": metrics.avg_time_processed,
        "max_time_processed": metrics.max_time_processed,
        "latest_file_processed_timestamp": (
            metrics.latest_file_processed_timestamp
        ),
        "avg_file_size": metrics.avg_file_size
    })


@api_view(['GET'])
def version(request):
    return Response({"version": VERSION})


class CollectionsViewSet(ModelViewSet):
    queryset = Collections.objects.all()
    permission_classes = (IsOwner,)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionsCreateSerializer
        return CollectionsSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Collections.objects.filter(owner=self.request.user)

    @action(detail=True, methods=('post',), url_path='(?P<document_id>[^/.]+)')
    def add_document(self, request, pk=None, document_id=None):
        try:
            collection = self.get_object()
            document = Document.objects.get(id=document_id)
            collection.documents.add(document)
            return Response(status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=('delete',), url_path='(?P<document_id>[^/.]+)')
    def remove_document(self, request, pk=None, document_id=None):
        try:
            collection = self.get_object()
            document = Document.objects.get(id=document_id)
            collection.documents.remove(document)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsOwner,)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action == 'list':
            return DocumentListSerializer
        return DocumentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
