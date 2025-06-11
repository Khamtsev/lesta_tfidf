import heapq
from collections import Counter, deque
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
def calculate_document_tfidf(document_text, collection_texts):
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
def calculate_collection_tfidf(collection_texts):
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


class HuffmanNode:
    """Узел дерева Хаффмана."""
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    """Строит дерево Хаффмана для текста."""
    freq = Counter(text)

    nodes = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(nodes)

    while len(nodes) > 1:
        left_child = heapq.heappop(nodes)
        right_child = heapq.heappop(nodes)
        merged_node = HuffmanNode(freq=left_child.freq + right_child.freq)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(nodes, merged_node)

    return nodes[0]


def build_huffman_codes(root):
    """Строит таблицу кодов Хаффмана."""
    codes = {}
    queue = deque([(root, "")])

    while queue:
        node, code = queue.popleft()

        if node.char is not None:
            codes[node.char] = code
            continue

        if node.left:
            queue.append((node.left, code + "0"))
        if node.right:
            queue.append((node.right, code + "1"))

    return codes


def huffman_encode(text):
    """Кодирует текст с помощью алгоритма Хаффмана."""
    if not text:
        return "", {}

    tree = build_huffman_tree(text)
    codes = build_huffman_codes(tree)
    encoded = "".join(codes[char] for char in text)

    return encoded, codes
