import pandas as pd
import termcolor
import random

guesses = pd.read_csv("guesses.txt", delimiter="\n")


def simulate():
    answer = get_random_answer()
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
    answers = pd.read_csv("answers.txt", delimiter="\n")
    id = random.randrange(len(answers.index))
    return answers["word"][id]

def get_guess() -> str:
    guess = input("guess: ")
    return guess

def validate(guess: str) -> bool:
    return guess in guesses["word"].values

def check(guess: str, answer: str) -> list[dict]:
    remaining_answer = list(answer)
    remaining_guess = list(guess)
    hint = ["on_grey" for _ in range(5)]
    for i in range(5):
        if guess[i] == answer[i]:
            hint[i] = "on_green"
            remaining_answer[i] = None
            remaining_guess[i] = None
    for i in range(5):
        if remaining_guess[i]:
            if remaining_guess[i] in remaining_answer:
                hint[i] = "on_yellow"
                remaining_answer[i] = None
                remaining_guess[i] = None
    return [
        termcolor.colored(text=guess[i], on_color=hint[i]) 
        for i in range(5)]
            



if __name__ == "__main__":
    simulate()