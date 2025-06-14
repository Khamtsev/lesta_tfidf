from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from core.models import (
    Collections,
    Document,
    DocumentMetrics,
    CollectionMetrics,
    CollectionDocument
)
from core.constants import VERSION
from core.services import (
    calculate_document_tfidf,
    calculate_collection_tfidf,
    huffman_encode
)
from core.etags import get_collection_etag
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


class OwnerViewSet(ModelViewSet):
    """Базовый ViewSet для объектов, принадлежащих пользователю."""
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.none()
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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

    doc_metrics_dict = doc_metrics.to_dict()
    doc_metrics_dict['total_documents'] = total_documents

    coll_metrics_dict = coll_metrics.to_dict()
    coll_metrics_dict['avg_documents_per_collection'] = round(
        avg_docs_per_collection, 3
    )

    return Response({
        "document_metrics": doc_metrics_dict,
        "collection_metrics": coll_metrics_dict
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def version(request):
    """Возвращает версию приложения."""
    return Response({"version": VERSION})


class CollectionViewSet(OwnerViewSet):
    """Представление для коллекций документов."""
    queryset = Collections.objects.all()
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionsCreateSerializer
        return CollectionsSerializer

    @swagger_auto_schema(
        operation_description="Возвращает статистику по коллекции",
        responses={
            200: "Статистика успешно получена",
            400: "Коллекция пуста"
        },
        security=[{'Bearer': []}],
        operation_id='collection_statistics'
    )
    def get_collection_statistics(self, request, pk=None):
        """Возвращает статистику по коллекции."""
        collection = self.get_object()

        etag = get_collection_etag(request, pk=pk)

        if_none_match = request.META.get('HTTP_IF_NONE_MATCH')
        if if_none_match and if_none_match == etag:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        documents = collection.documents.all()
        if not documents:
            return Response(
                {"error": "Collection is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        texts = [doc.content for doc in documents]
        stats = calculate_collection_tfidf(texts)
        sorted_stats = sorted(stats, key=lambda x: x['tf'])[
            :settings.DISPLAYED_WORDS
        ]
        serializer = StatisticsSerializer({'statistics': sorted_stats})
        response = Response(serializer.data)
        response['ETag'] = etag
        return response

    @swagger_auto_schema(
        operation_description="Добавляет документ в коллекцию",
        responses={
            200: "Документ успешно добавлен в коллекцию",
            404: "Документ не найден"
        },
        security=[{'Bearer': []}],
        operation_id='add_document'
    )
    def create_document(self, request, pk=None, document_id=None):
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

    @swagger_auto_schema(
        operation_description="Удаляет документ из коллекции",
        responses={
            204: "Документ успешно удален из коллекции",
            404: "Документ не найден"
        },
        security=[{'Bearer': []}],
        operation_id='remove_document'
    )
    def destroy_document(self, request, pk=None, document_id=None):
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


class DocumentViewSet(OwnerViewSet):
    """Представление для документов."""
    queryset = Document.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action == 'list':
            return DocumentListSerializer
        return DocumentDetailSerializer

    @swagger_auto_schema(
        operation_description="Возвращает статистику по документу",
        responses={
            200: "Статистика успешно получена",
            400: "Документ не находится ни в одной коллекции"
        },
        security=[{'Bearer': []}],
        operation_id='document_statistics'
    )
    def get_document_statistics(self, request, pk=None):
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
            stats = calculate_document_tfidf(document.content, texts)
            sorted_stats = sorted(stats, key=lambda x: x['tf'])[:settings.DISPLAYED_WORDS]

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

    @swagger_auto_schema(
        operation_description="Возвращает содержимое документа, закодированное кодом Хаффмана",
        responses={
            200: "Документ успешно закодирован",
            404: "Документ не найден"
        },
        security=[{'Bearer': []}],
        operation_id='document_huffman'
    )
    def get_huffman(self, request, pk=None):
        """Возвращает содержимое документа, закодированное кодом Хаффмана."""
        document = self.get_object()
        encoded_text, codes = huffman_encode(document.content)

        return Response({
            'encoded_text': encoded_text,
            'codes': codes
        })
