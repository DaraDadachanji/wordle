from tkinter import W
import pandas as pd
import numpy as np
import copy
import game

def assist_guesses():
    guesser = Guesser()
    while True:
        hint = get_hint()
        guesser.give_hint(hint)
        guesser.print_remaining_answers()


class Guesser:
    def __init__(self) -> None:
        self.hints: list[game.Word] = []
        #self.guesses = pd.read_csv("src/guesses.txt", delimiter="\n")
        self.answers = pd.read_csv("src/answers.txt", delimiter="\n")

    def give_hint(self, hint: game.Word):
        self.hints.append(hint)
        validator = np.vectorize(check, otypes=[bool], excluded=["hint"])
        remaining = validator(answer=self.answers["word"], hint=hint)
        self.answers = self.answers[remaining]

    def print_remaining_answers(self):
        print(self.answers["word"].to_list())


def create_hint(word: str, pattern: str):
    hint = game.Word(word)
    for i in range(5):
        if pattern[i] == "c":
            hint[i].state = game.State.CORRECT
        elif pattern[i] == "p":
            hint[i].state = game.State.PRESENT
        elif pattern[i] == "a":
            hint[i].state = game.State.ABSENT
        else:
            raise NotImplementedError
    return hint


def check(answer: str, hint: game.Word) -> bool:
    _hint = copy.deepcopy(hint)
    w_answer = game.Word(answer)
    for i in range(5):
        if _hint[i].rune == answer[i]:
            if _hint[i].state != game.State.CORRECT:
                return False
            w_answer[i].accounted_for = True
            _hint[i].accounted_for = True
    for i in range(5):
        if not _hint[i].accounted_for:
            if w_answer.contains(_hint[i].rune):
                if _hint[i].state != game.State.PRESENT:
                    return False
            else:
                if _hint[i].state != game.State.ABSENT:
                    return False
    return True


def get_hint():
    guess = input("Guess: ")
    pattern = input("Pattern: ")
    hint = create_hint(word=guess, pattern=pattern)
    return hint


if __name__ == "__main__":
    assist_guesses()
