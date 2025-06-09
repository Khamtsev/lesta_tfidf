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
