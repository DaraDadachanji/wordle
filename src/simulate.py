
import tkinter
import pandas as pd
import termcolor
import random
import enum

guesses = pd.read_csv("src/guesses.txt", delimiter="\n")

CORRECT_COLOR = "green"
ABSENT_COLOR = "white"
PRESENT_COLOR = "magenta"


def simulate():
    answer = get_random_answer()
    while True:
        guess = get_guess()
        if validate(guess):
            hint = check(guess=guess, answer=answer)
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


def validate(guess: str) -> bool:
    return guess in guesses["word"].values

class State(enum.Enum):
    CORRECT = 2
    PRESENT = 1
    ABSENT = 0


class Letter:
    def __init__(self, letter: str) -> None:
        self.rune = letter
        self.state = State.ABSENT
        self.accounted_for = False
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Letter):
            return __o.rune == self.rune
        elif isinstance(__o, str):
            return __o == self.rune
        else:
            return False

    def mark_correct(self):
        self.state = State.CORRECT
        self.accounted_for = True

    def mark_present(self):
        self.state = State.PRESENT
        self.accounted_for = True



class Word(list[Letter]):
    def __init__(self, word: str) -> None:
        letters: list[Letter] = [Letter(letter) for letter in word]
        super(Word, self).__init__()
        self.extend(letters)
    
    def contains(self, check: Letter) -> bool:
        for letter in self:
            if not letter.accounted_for:
                if check == letter:
                    letter.accounted_for = True
                    return True



def check(guess: str, answer: str) -> list[tkinter.Text]:
    w_answer = Word(answer)
    hint = Word(guess)
    for i in range(5):
        if hint[i] == answer[i]:
            hint[i].mark_correct()
            w_answer[i].accounted_for = True
    for i in range(5):
        if not hint[i].accounted_for:
            if w_answer.contains(hint[i]):
                hint[i].mark_present()
    return hint


def render(hint: Word):
    highlights = {
        State.CORRECT: "on_green",
        State.PRESENT: "on_yellow",
        State.ABSENT: "on_grey"
    }
    text_colors = {
        State.CORRECT: "grey",
        State.PRESENT: "grey",
        State.ABSENT: "white"
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