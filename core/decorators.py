import time
from django.utils import timezone
from functools import wraps
from .models import Metrics


def timeit_decorator(func):
    """
    Декоратор для отслеживания времени выполнения функции
    и сохранения соответствующих метрик в базе данных.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        metrics, created = Metrics.objects.get_or_create(pk=1)
        metrics.latest_file_processed_timestamp = timezone.now()
        if metrics.min_time_processed == 0 or (
            execution_time < metrics.min_time_processed
        ):
            metrics.min_time_processed = execution_time
        if execution_time > metrics.max_time_processed:
            metrics.max_time_processed = execution_time
        metrics.total_time_processed += execution_time
        metrics.avg_time_processed = (
            metrics.total_time_processed / metrics.files_processed
        )
        metrics.avg_file_size = metrics.files_size / metrics.files_processed
        metrics.save()

        return result
    return wrapper
