from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Metrics
from core.constants import VERSION


@api_view(['GET'])
def status(request):
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
