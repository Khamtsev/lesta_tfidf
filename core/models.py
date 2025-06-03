from django.db import models


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
