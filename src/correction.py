from utils import get_word_counts, get_dictionary

LETTERS = "abcdefghijklmnopqrstuvwxyz"
WORD_COUNTS = get_word_counts()
DICTIONARY = get_dictionary()


def probability_of(word):
    return WORD_COUNTS[word] / sum(WORD_COUNTS.values())


def correct(word):
    return max(get_candidates(word), key=probability_of)


def get_candidates(word):
    # If the word is in the dictionary, no need to correct it
    if word in DICTIONARY:
        return [word]

    # If we have words that are one edit away and in the dictionary, return those
    first_edits = filter_unknown(one_edit_from(word))
    if len(first_edits) != 0:
        return first_edits

    # If we have words that are two edits away and in the dictionary, return those
    second_edits = filter_unknown(two_edits_from(word))
    if len(second_edits) != 0:
        return second_edits

    # Otherwise, just return the original word as we couldn't find a candidate
    return [word]


def filter_unknown(words):
    known_words = []
    for word in words:
        if word in DICTIONARY:
            known_words.append(word)
    return set(known_words)


def one_edit_from(word):
    # Generates splits of a word ex. "dog" -> [("", "dog"), ("d", "og"), ("do", "g"), ("dog", "")]
    splits = []
    for i in range(len(word) + 1):
        split = (word[:i], word[i:])
        splits.append(split)

    edits = []

    # Deletes ex. "dog" -> ["og", "dg", "do"]
    for (left, right) in splits:
        if right:
            deleted = left + right[1:]
            edits.append(deleted)

    # Swaps ex. "dog" -> ["odg", "dgo"]
    for (left, right) in splits:
        if len(right) > 1:
            swapped = left + right[1] + right[0] + right[2:]
            edits.append(swapped)

    # Substitutes ex. "dog" -> ["aog", "dag", "doa",  ...]
    for (left, right) in splits:
        for sub in LETTERS:
            substituted = left + sub + right[1:]
            edits.append(substituted)

    # Inserts ex. "cat" -> ["acat", "caat", "caat", "cata", ...]
    for (left, right) in splits:
        for insert in LETTERS:
            inserted = left + insert + right
            edits.append(inserted)

    # Convert from list to set to remove duplicates
    return list(set(edits))


def two_edits_from(word):
    # Find all words one edit away
    first_edits = one_edit_from(word)

    # Find all words one edit away from the first edits
    second_edits = set()
    for first_edit in first_edits:
        second_edits.update(one_edit_from(first_edit))

    all_edits = first_edits.union(second_edits)

    return all_edits


misspellings = ["speling", "computinga", "clasrom", "ptyhon", "prgrammin", "jonahtan"]
for misspelling in misspellings:
    print(f"{misspelling} -> {correct(misspelling)}")
