from utils import get_word_counts, get_words

LETTERS = "abcdefghijklmnopqrstuvwxyz"
WORD_COUNTS = get_word_counts()
WORDS = get_words()


def probability_of(word):
    return WORD_COUNTS[word] / sum(WORD_COUNTS.values())


def correct(word):
    return max(get_candidates(word), key=probability_of)


def get_candidates(word):
    if word in WORDS:
        return [word]
    
    return (
        filter_unknown(one_edit_from(word))
        or filter_unknown(two_edits_from(word))
        or [word]
    )


def filter_unknown(words):
    return set(word for word in words if word in WORDS)


def one_edit_from(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [l + r[1:] for (l, r) in splits if r]
    transposes = [l + r[1] + r[0] + r[2:] for (l, r) in splits if len(r) > 1]
    replaces = [l + x + r[1:] for (l, r) in splits for x in LETTERS]
    inserts = [l + x + r for (l, r) in splits for x in LETTERS]

    return set(deletes + transposes + replaces + inserts)


def two_edits_from(word):
    return set(
        second_edit
        for edit in one_edit_from(word)
        for second_edit in one_edit_from(edit)
    )


misspellings = ["speling", "computinga", "clasrom", "ptyhon", "prgrammin", "jonahtan"]
for misspelling in misspellings:
    print(f"{misspelling} -> {correct(misspelling)}")
