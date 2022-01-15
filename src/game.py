import pandas as pd
import enum

guesses = pd.read_csv("src/guesses.txt", delimiter="\n")

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
        return False


def check(guess: str, answer: str) -> Word:
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