from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from core.models import (
    Collections,
    Document,
    DocumentMetrics,
    CollectionMetrics
)
from core.constants import VERSION, DISPLAYED_WORDS
from core.services import get_document_statistics, get_collection_statistics
from .serializers import (
    CollectionsCreateSerializer,
    CollectionsSerializer,
    DocumentListSerializer,
    DocumentDetailSerializer,
    DocumentCreateSerializer,
    StatisticsSerializer,
    CollectionStatisticsSerializer
)
from users.permissions import IsOwner


@api_view(['GET'])
@permission_classes([AllowAny])
def check_status(request):
    """Проверяет статус сервера."""
    return Response({"status": "OK"})


@api_view(['GET'])
@permission_classes([AllowAny])
def metrics(request):
    """Возвращает метрики системы."""
    doc_metrics, _ = DocumentMetrics.objects.get_or_create(pk=1)
    coll_metrics, _ = CollectionMetrics.objects.get_or_create(pk=1)

    total_documents = Document.objects.count()
    total_collections = Collections.objects.count()
    avg_docs_per_collection = (
        total_documents / total_collections if total_collections > 0 else 0
    )

    return Response({
        "document_metrics": {
            "statistics_requests": doc_metrics.statistics_requests,
            "latest_statistics_processed_timestamp": (
                doc_metrics.latest_statistics_processed_timestamp
            ),
            "min_time_processed": round(doc_metrics.min_time_processed, 3),
            "avg_time_processed": round(doc_metrics.avg_time_processed, 3),
            "max_time_processed": round(doc_metrics.max_time_processed, 3),
            "total_documents": total_documents
        },
        "collection_metrics": {
            "statistics_requests": coll_metrics.statistics_requests,
            "latest_statistics_processed_timestamp": (
                coll_metrics.latest_statistics_processed_timestamp
            ),
            "min_time_processed": round(coll_metrics.min_time_processed, 3),
            "avg_time_processed": round(coll_metrics.avg_time_processed, 3),
            "max_time_processed": round(coll_metrics.max_time_processed, 3),
            "avg_documents_per_collection": round(avg_docs_per_collection, 3)
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def version(request):
    """Возвращает версию приложения."""
    return Response({"version": VERSION})


class CollectionViewSet(ModelViewSet):
    """Представление для коллекций документов."""
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

    def get_collection_statistics(self, request, pk=None):
        """Возвращает статистику по коллекции."""
        collection = self.get_object()
        documents = collection.documents.all()
        if not documents:
            return Response(
                {"error": "Collection is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        texts = [doc.content for doc in documents]
        stats = get_collection_statistics(texts)
        sorted_stats = sorted(stats, key=lambda x: x['tf'])[:DISPLAYED_WORDS]
        serializer = StatisticsSerializer({'statistics': sorted_stats})
        return Response(serializer.data)

    @action(detail=True, methods=('post',), url_path='(?P<document_id>[^/.]+)')
    def add_document(self, request, pk=None, document_id=None):
        """Добавляет документ в коллекцию."""
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
        """Удаляет документ из коллекции."""
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
    """Представление для документов."""
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

    @action(detail=True)
    def statistics(self, request, pk=None):
        """Возвращает статистику по документу."""
        document = self.get_object()
        collections = document.collections.all()
        if not collections:
            return Response(
                {"error": "Document is not in any collection"},
                status=status.HTTP_400_BAD_REQUEST
            )

        collections_stats = []
        for collection in collections:
            texts = [doc.content for doc in collection.documents.all()]
            stats = get_document_statistics(document.content, texts)
            sorted_stats = sorted(stats, key=lambda x: x['tf'])[:DISPLAYED_WORDS]

            collections_stats.append({
                'collection_id': collection.id,
                'collection_name': collection.name or f"Collection {collection.id}",
                'statistics': sorted_stats
            })

        serializer = CollectionStatisticsSerializer(
            collections_stats,
            many=True
        )
        return Response(serializer.data)
