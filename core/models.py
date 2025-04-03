from django.db import models


class DocumentCount(models.Model):
    count = models.IntegerField(default=0)


class Word(models.Model):
    word = models.CharField(max_length=255)
    in_docs = models.IntegerField(default=0)

    def __str__(self):
        return self.word
