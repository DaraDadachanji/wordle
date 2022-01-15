
import pandas as pd
import termcolor
import random
import wordle


def simulate():
    answer = get_random_answer()
    while True:
        guess = get_guess()
        if wordle.validate(guess):
            hint = wordle.check(guess=guess, answer=answer)
            render(hint)
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


def render(hint: wordle.Word):
    highlights = {
        wordle.State.CORRECT: "on_green",
        wordle.State.PRESENT: "on_yellow",
        wordle.State.ABSENT: "on_grey"
    }
    text_colors = {
        wordle.State.CORRECT: "grey",
        wordle.State.PRESENT: "grey",
        wordle.State.ABSENT: "white"
    }
    output = []
    for letter in hint:
        output.append(
            termcolor.colored(
                text=letter.rune,
                color=text_colors[letter.state],
                on_color=highlights[letter.state]
            )
        )
    print(*output)    


if __name__ == "__main__":
    simulate()