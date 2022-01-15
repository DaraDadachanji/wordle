
import pandas as pd
import termcolor
import random
import game


def simulate():
    answer = get_random_answer()
    while True:
        guess = get_guess()
        if game.validate(guess):
            hint = game.check(guess=guess, answer=answer)
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


def render(hint: game.Word):
    highlights = {
        game.State.CORRECT: "on_green",
        game.State.PRESENT: "on_yellow",
        game.State.ABSENT: "on_grey"
    }
    text_colors = {
        game.State.CORRECT: "grey",
        game.State.PRESENT: "grey",
        game.State.ABSENT: "white"
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