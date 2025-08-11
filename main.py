#!/usr/bin/env python3
"""
File Selector for Cleaned Text Files
- Lists all cleaned files in ROOT_PATH.
- Lets the user pick one by number.
- Returns the Path object for the chosen file.
"""
import random
from pathlib import Path

# === SETTINGS ===
ROOT_PATH = Path('.')            # Directory to search
PATTERN = '*.txt'                # File pattern to match
CLEANED_TAG = '.cleaned'         # Tag to mark cleaned files
EXCLUDE_DIRS = {'.git', 'venv', '__pycache__', '.venv', 'env', 'node_modules'}


def iter_cleaned_files(root: Path, pattern: str):
    files = root.rglob(pattern)
    for p in files:
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if CLEANED_TAG in p.stem:
            yield p


def select_cleaned_file() -> Path | None:
    files = list(iter_cleaned_files(ROOT_PATH, PATTERN))
    if not files:
        print("No cleaned files found.")
        return None
    print("Select a cleaned file:")
    for idx, f in enumerate(files, 1):
        print(f"{idx}. {str(f).replace(".cleaned", "")}")
    while True:
        choice = input("Enter file number ('exit' to stop): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files):
                return files[idx - 1]
        elif choice == "exit":
            return None
        print("Invalid choice. Please try again.")


def is_ending_word(word):
    punctuation = ['.', '!', '?']
    if not any(p in word for p in punctuation):
        return False
    if not any(word[-1] == p for p in punctuation):
        return False
    if word in ["e.g.", "i.e.", "p.", "pp.", "Inc.", "etc."]:
        return False
    if len(word) <= 2:
        return False

    return True


def get_random_instance(word, words):
    indices = []
    for i in range(len(words)):
        for j in range(len(words[i])):
            if words[i][j] == word:
                indices.append((i,j))
    return random.choice(indices)


def generate_sentence(file_path):
    # setup separated sentences and words
    sentences = []
    words = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            sentences.append(line.strip())

    for i in range(len(sentences)):
        words.append([])
        for w in sentences[i].split(" "):
            words[i].append(w)

    # construct sentence
    sentence = ""
    index = (random.randrange(len(words)), 0)
    word = words[index[0]][0]
    sentence += word

    try:
        while not is_ending_word(word):
            sentence += " "
            next_word = words[index[0]][index[1]+1]
            index = get_random_instance(next_word, words)
            word = words[index[0]][index[1]]
            sentence += word
        print(sentence, end="")
    except IndexError:
        print(f"[oops! something went wrong with the word '{word}'!]")



def main():
    selected = select_cleaned_file()
    while selected:
        print()
        print(f"Generating from source: {selected}")
        print("Press Enter to make another")
        print("Type anything to change source")
        print()
        generate_sentence(selected)
        while input().strip() == "":
            generate_sentence(selected)
        print()
        selected = select_cleaned_file()


if __name__ == '__main__':
    main()
