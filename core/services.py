from collections import Counter
import re
import math
from .models import DocumentMetrics, CollectionMetrics
from .decorators import metrics_decorator


def tokenize(text):
    """Разбивает текст на токены (слова)."""
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def calculate_tf(text):
    """Рассчитывает TF для текста."""
    words = tokenize(text)
    word_count = Counter(words)
    total_words = len(words)

    return {word: count/total_words for word, count in word_count.items()}


def calculate_idf(documents):
    """Рассчитывает IDF для списка документов."""

    doc_freq = Counter()
    for doc in documents:
        unique_words = set(tokenize(doc))
        doc_freq.update(unique_words)

    total_docs = len(documents)
    return {
        word: math.log(total_docs / count)
        for word, count in doc_freq.items()
    }


@metrics_decorator(DocumentMetrics)
def get_document_statistics(document_text, collection_texts):
    """Получает статистику по документу с учетом коллекции."""
    tf = calculate_tf(document_text)
    idf = calculate_idf(collection_texts)

    return [
        {
            'word': word,
            'tf': tf[word],
            'idf': idf[word]
        }
        for word in tf
    ]


@metrics_decorator(CollectionMetrics)
def get_collection_statistics(collection_texts):
    """Получает статистику по коллекции."""
    combined_text = ' '.join(collection_texts)
    tf = calculate_tf(combined_text)
    idf = calculate_idf(collection_texts)

    return [
        {
            'word': word,
            'tf': tf[word],
            'idf': idf[word]
        }
        for word in tf
    ]
