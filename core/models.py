from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MetricsBase(models.Model):
    """Базовая абстрактная модель для метрик."""
    statistics_requests = models.PositiveIntegerField(default=0)
    latest_statistics_processed_timestamp = models.DateTimeField(null=True, blank=True)
    min_time_processed = models.FloatField(default=0.0)
    total_time_processed = models.FloatField(default=0.0)
    avg_time_processed = models.FloatField(default=0.0)
    max_time_processed = models.FloatField(default=0.0)

    class Meta:
        abstract = True

    def to_dict(self):
        """Преобразует модель в словарь."""
        return {
            'statistics_requests': self.statistics_requests,
            'latest_statistics_processed_timestamp': (
                self.latest_statistics_processed_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                if self.latest_statistics_processed_timestamp
                else None
            ),
            'min_time_processed': round(self.min_time_processed, 3),
            'avg_time_processed': round(self.avg_time_processed, 3),
            'max_time_processed': round(self.max_time_processed, 3),
        }


class DocumentMetrics(MetricsBase):
    """Метрики для документов."""
    pass


class CollectionMetrics(MetricsBase):
    """Метрики для коллекций."""
    pass


class Collections(models.Model):
    """Коллекции документов."""
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections'
    )

    def __str__(self):
        return self.name or f"Collection {self.id}"


class Document(models.Model):
    """Документы."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    collections = models.ManyToManyField(Collections, related_name='documents')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    def __str__(self):
        return self.title
