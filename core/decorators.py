import time
from django.utils import timezone
from functools import wraps


class metrics_decorator:
    """
    Декоратор для отслеживания времени обработки и сохранения метрик.

    Args:
        metrics_model: Модель метрик (DocumentMetrics или CollectionMetrics)
    """
    def __init__(self, metrics_model):
        self.metrics_model = metrics_model

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            metrics, created = self.metrics_model.objects.get_or_create(pk=1)

            metrics.statistics_requests += 1
            metrics.latest_statistics_processed_timestamp = timezone.now()

            if metrics.min_time_processed == 0 or (
                execution_time < metrics.min_time_processed
            ):
                metrics.min_time_processed = execution_time

            if execution_time > metrics.max_time_processed:
                metrics.max_time_processed = execution_time

            metrics.total_time_processed += execution_time
            metrics.avg_time_processed = (
                metrics.total_time_processed / metrics.statistics_requests
            )
            metrics.save()

            return result
        return wrapper
