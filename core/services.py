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

    def __str__(self):
        return f"({self.char}, {self.freq})"


def counting_sort(nodes):
    """
    Сортировка подсчетом для списка HuffmanNode по частоте (freq).
    """
    if not nodes:
        return []

    max_freq = max(node.freq for node in nodes)
    count = [0] * (max_freq + 1)

    for node in nodes:
        count[node.freq] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    result = [None] * len(nodes)

    for node in reversed(nodes):
        count[node.freq] -= 1
        result[count[node.freq]] = node

    return result


def build_huffman_tree(text):
    """Создает дерево Хаффмана из текста."""
    if not text:
        return None

    freq_dict = {}
    for char in text:
        freq_dict[char] = freq_dict.get(char, 0) + 1

    if len(freq_dict) == 1:
        char = list(freq_dict.keys())[0]
        return HuffmanNode(char=char, freq=freq_dict[char])

    nodes = [HuffmanNode(char=char, freq=freq) 
             for char, freq in freq_dict.items()]

    n = len(nodes)
    sorted_nodes = counting_sort(nodes)
    sum_nodes = [HuffmanNode(char=None, freq=float('inf'))] * (n - 1)

    i = 0  # указатель на текущий узел в sorted_nodes
    j = 0  # указатель на текущий узел в sum_nodes
    k = 0  # указатель на место для нового суммированного узла

    while i < n - 1 or j < k:
        min1 = min2 = None

        if i < n and (j >= k or sorted_nodes[i].freq <= sum_nodes[j].freq):
            min1 = sorted_nodes[i]
            i += 1
        elif j < k:
            min1 = sum_nodes[j]
            j += 1
        else:
            break

        if i < n and (j >= k or sorted_nodes[i].freq <= sum_nodes[j].freq):
            min2 = sorted_nodes[i]
            i += 1
        elif j < k:
            min2 = sum_nodes[j]
            j += 1
        else:
            break

        new_node = HuffmanNode(char=None, freq=min1.freq + min2.freq)
        new_node.left = min1
        new_node.right = min2

        sum_nodes[k] = new_node
        k += 1

    return sum_nodes[k-1] if k > 0 else sorted_nodes[0]


def build_huffman_codes(root):
    """Создает словарь с кодами Хаффмана для каждого символа."""
    codes = {}
    if root is None:
        return codes

    if root.char is not None and root.left is None and root.right is None:
        codes[root.char] = "0"
        return codes

    stack = [(root, "")]

    while stack:
        node, code = stack.pop()

        if node.char is not None:
            codes[node.char] = code
            continue

        if node.right:
            stack.append((node.right, code + "1"))

        if node.left:
            stack.append((node.left, code + "0"))

    return codes


def huffman_encode(text):
    """Кодирует текст с помощью алгоритма Хаффмана."""
    if not text:
        return "", {}

    tree = build_huffman_tree(text)
    codes = build_huffman_codes(tree)
    encoded = "".join(codes[char] for char in text)

    return encoded, codes
