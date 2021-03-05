import re
from collections import Counter
from typing import List
import random


def only_words(text: str):
    return re.findall(r"\w+", text.lower())

def get_words():
    with open("./src/datasets/dictionary.txt") as reader:
        return set(only_words(reader.read()))


def get_word_counts():
    with open("./src/datasets/corpus.txt") as reader:
        return Counter(only_words(reader.read()))


LETTERS = "abcdefghijklmnopqrstuvwxyz"
WORD_COUNTS = get_word_counts()
WORDS = get_words()

def probability_of(word: str):
    return WORD_COUNTS[word] / sum(WORD_COUNTS.values())


def correct(word):
    return max(get_candidates(word), key=probability_of)


def get_candidates(word: str):
    if word in WORDS:
        return [word]
    else:
        return (
            filter_unknown(one_edit_from(word))
            or filter_unknown(two_edits_from(word))
            or [word]
        )


def filter_unknown(words: List[str]):
    return set(word for word in words if word in WORDS)


def one_edit_from(word: str):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [l + r[1:] for (l, r) in splits if r]
    transposes = [l + r[1] + r[0] + r[2:] for (l, r) in splits if len(r) > 1]
    replaces = [l + x + r[1:] for (l, r) in splits for x in LETTERS]
    inserts = [l + x + r for (l, r) in splits for x in LETTERS]

    return set(deletes + transposes + replaces + inserts)


def two_edits_from(word: str):
    return set(
        second_edit
        for edit in one_edit_from(word)
        for second_edit in one_edit_from(edit)
    )


def get_misspellings():
    with open("./src/datasets/misspellings.txt") as reader:
        text = reader.read().split("\n")
        base_indexes = [text.index(word) for word in text if word[0] == "$"]
        misspellings = []
        for i, word in enumerate(text):
            if word[0] == "$":
                pass

            j = i
            while not j in base_indexes:
                j -= 1
            misspellings.append((word.lower(), text[j][1:].lower()))

    return misspellings


def test(misspellings):
    results = {"right": 0, "wrong": 0}

    for wrong, right in misspellings:
        correction = correct(wrong)
        if correction == right:
            results["right"] += 1
        else:
            results["wrong"] += 1

    percentage = round((results["right"] / sum(results.values())) * 100)
    print(f"Was right {percentage}% of the time")
        

misspellings = get_misspellings()
random.shuffle(misspellings)
sample = misspellings[:1000]
print("Built misspellings")
test(sample)