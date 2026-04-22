with open("ValidWords.txt", "r") as f:
    data = [line.strip() for line in f.readlines()]
    print(all([len(word) == 5 for word in data]))