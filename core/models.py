from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentCount(models.Model):
    count = models.IntegerField(default=0)


class Metrics(models.Model):
    files_processed = models.PositiveIntegerField(default=0)
    min_time_processed = models.FloatField(default=0.0)
    total_time_processed = models.FloatField(default=0.0)
    avg_time_processed = models.FloatField(default=0.0)
    max_time_processed = models.FloatField(default=0.0)
    latest_file_processed_timestamp = models.DateTimeField(null=True, blank=True)
    files_size = models.PositiveIntegerField(default=0)
    avg_file_size = models.FloatField(default=0.0)


class Word(models.Model):
    word = models.CharField(max_length=255)
    in_docs = models.IntegerField(default=0)

    def __str__(self):
        return self.word


class Collections(models.Model):
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
