import pandas as pd
import numpy as np


def sandbox():
    alphabet = getAlphabetValues()
    print(alphabet)
    guesses = pd.read_csv("guesses.txt", delimiter="\n")
    v_get_word_value = np.vectorize(getWordValue,otypes=[int], excluded=["alphabet"])
    guesses["value"] = v_get_word_value(guesses["word"], alphabet)
    best_guesses = guesses.sort_values(by=["value"], ascending=False)
    print(best_guesses.head())

def getAlphabetValues() -> dict[str,int]:
    answers = pd.read_csv("answers.txt", delimiter="\n")
    total = len(answers.index)
    print(f"Total answers: {total}")
    alphabet = {letter:0 for letter in "abcdefghijklmnopqrstuvwxyz"}
    for letter in alphabet: #["a", "e", "i", "o", "u"]:
        count = len(answers[answers['word'].str.contains(letter)].index)
        alphabet[letter] = count
    return alphabet


def getWordValue(word: str, alphabet: dict[str,int]):
    value = 0
    for letter in set(word):
        value += alphabet[letter]
    return value

if __name__ == "__main__":
    sandbox()
