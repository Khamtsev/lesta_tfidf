from core.models import Collections, CollectionDocument


def get_collection_etag(request, pk):
    """Генерирует ETag для коллекции."""
    collection = Collections.objects.get(pk=pk)
    document_timestamps = CollectionDocument.objects.filter(
        collection=collection
    ).values_list('created_at', flat=True)
    etag_content = f"{collection.id}-{'-'.join(str(ts) for ts in document_timestamps)}"
    return f'"{hash(etag_content)}"'
