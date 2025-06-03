from collections import Counter
from .decorators import timeit_decorator
from .models import DocumentCount, Metrics, Word
import re
import math


@timeit_decorator
def calculate_tf_idf(doc):
    text = doc.file.read().decode('utf-8')
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_text.split()

    total_words = len(words)

    word_counter = Counter(words)
    tf = {word: count / total_words for word, count in word_counter.items()}

    idf = {}
    metrics, created = Metrics.objects.get_or_create(pk=1)
    metrics.files_processed += 1
    metrics.save()

    results = []

    for word in word_counter:
        word_obj, created = Word.objects.get_or_create(word=word)
        word_obj.in_docs += 1
        word_obj.save()

        idf[word] = math.log(metrics.files_processed / word_obj.in_docs)
        results.append((word, tf[word], idf[word], tf[word]*idf[word]))

    return results
