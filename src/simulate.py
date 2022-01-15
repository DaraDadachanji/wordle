import tkinter
import pandas as pd
import termcolor
import random

guesses = pd.read_csv("src/guesses.txt", delimiter="\n")

CORRECT_COLOR = "on_green"
WRONG_COLOR = "on_grey"
ALMOST_COLOR = "on_magenta"


def simulate():
    answer = get_random_answer()
    print(answer)
    while True:
        guess = get_guess()
        if validate(guess):
            hint = check(guess=guess, answer=answer)
            print(*hint)
            if guess == answer:
                break
        else:
            print("invalid guess")

def get_random_answer() -> str:
    answers = pd.read_csv("src/answers.txt", delimiter="\n")
    id = random.randrange(len(answers.index))
    return answers["word"][id]


def get_guess() -> str:
    guess = input("guess: ")
    return guess


def validate(guess: str) -> bool:
    return guess in guesses["word"].values


def check(guess: str, answer: str) -> list[tkinter.Text]:
    remaining_answer = list(answer)
    remaining_guess = list(guess)
    hint = [WRONG_COLOR for _ in range(5)]
    for i in range(5):
        if guess[i] == answer[i]:
            hint[i] = CORRECT_COLOR
            remaining_answer[i] = None
            remaining_guess[i] = None
    for i in range(5):
        if remaining_guess[i]:
            if remaining_guess[i] in remaining_answer:
                hint[i] = ALMOST_COLOR
                remaining_guess[i] = None
                for j, letter in enumerate(remaining_answer):
                    if letter == remaining_guess[i]:
                        remaining_answer[i] = None
    return [
        termcolor.colored(text=guess[i], on_color=hint[i]) 
        for i in range(5)]


if __name__ == "__main__":
    simulate()