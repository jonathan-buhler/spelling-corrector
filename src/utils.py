import re
from collections import Counter
from random import shuffle


def only_words(text: str):
    return re.findall(r"[^_\W]+", text.lower())


def get_misspellings():
    with open("./src/datasets/misspellings.txt") as reader:
        lines = reader.read().split("\n")
        pairs = [line.split(",") for line in lines]
        shuffle(pairs)
        return pairs

def get_words():
    with open("./src/datasets/dictionary.txt") as reader:
        return set(only_words(reader.read()))


def get_word_counts():
    with open("./src/datasets/corpus.txt") as reader:
        return Counter(only_words(reader.read()))
