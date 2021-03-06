def get_misspellings():
    with open("./src/datasets/misspellings.txt") as lines:
        for line in lines:
            print(line)

    # return misspellings
