def get_misspellings():
    with open("./src/datasets/misspellings.txt") as reader:
        text = reader.read().split("\n")
        base_indexes = [text.index(word) for word in text if word[0] == "$"]
        misspellings = []
        for i, word in enumerate(text):
            if word[0] == "$":
                continue

            j = i
            while not j in base_indexes:
                j -= 1
            misspellings.append((word.lower(), text[j][1:].lower()))

    return misspellings


misspellings = get_misspellings()
print(misspellings[:10])

with open("./src/datasets/new_misspellings.txt", "a") as writer:
    for misspelling in misspellings:
        writer.write(f"{misspelling[0]},{misspelling[1]}\n")