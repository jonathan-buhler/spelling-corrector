import re
from collections import Counter
from random import shuffle
from os import listdir


def only_words(text: str):
    return re.findall(r"[^_\W]+", text.lower())


def get_misspellings():
    with open("./src/datasets/misspellings.txt") as reader:
        lines = reader.read().split("\n")
        pairs = [line.split(",") for line in lines]
        shuffle(pairs)
        return pairs

def get_words():
    with open("./datasets/dictionary.txt") as reader:
        return set(only_words(reader.read()))


def get_word_counts():
    with open("./datasets/corpus.txt") as reader:
        return Counter(only_words(reader.read()))

def collate():
    files = listdir("./datasets/gutenberg")
    shuffle(files)
    with open("./datasets/corpus.txt", "w") as outfile:
        for file in files[:512]:
            with open(f"./datasets/gutenberg/{file}") as infile:
                for line in infile:
                    outfile.write(line)