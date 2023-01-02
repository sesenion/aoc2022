from dataclasses import dataclass
from enum import Enum, auto


class Hand(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


@dataclass
class Rock:
    hand: Hand = Hand.Rock
    defeats: Hand = Hand.Scissors


@dataclass
class Paper:
    hand: Hand = Hand.Paper
    defeats: Hand = Hand.Rock


@dataclass
class Scissors:
    hand: Hand = Hand.Scissors
    defeats: Hand = Hand.Paper


def translate_symbol(symbol: str) -> Rock | Paper | Scissors:
    return {
        "A": Rock(),
        "B": Paper(),
        "C": Scissors(),
        "X": Rock(),
        "Y": Paper(),
        "Z": Scissors(),
    }[symbol]


def translate_outcome(symbol: str):
    def lose(other_hand: Rock | Paper | Scissors) -> Rock | Paper | Scissors:
        match other_hand:
            case Rock():
                return Scissors
            case Paper():
                return Rock
            case Scissors():
                return Paper

    def win(other_hand: Rock | Paper | Scissors) -> Rock | Paper | Scissors:
        match other_hand:
            case Rock():
                return Paper
            case Paper():
                return Scissors
            case Scissors():
                return Rock

    def draw(other_hand: Rock | Paper | Scissors) -> Rock | Paper | Scissors:
        return other_hand

    return {"X": lose,
            "Y": draw,
            "Z": win}[symbol]


def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


def get_score(other: Hand, mine: Hand) -> int:
    if mine.defeats == other.hand:
        return 6 + mine.hand.value

    if other.defeats == mine.hand:
        return mine.hand.value

    return 3 + mine.hand.value


def task1():
    score = 0
    for line in get_input():
        other, mine = (translate_symbol(symbol) for symbol in line.split())
        score += get_score(other, mine)
    return score


def task2():
    score = 0
    for line in get_input():
        other, outcome = line.split()
        other = translate_symbol(other)
        mine = translate_outcome(outcome)(other)
        score += get_score(other, mine)
    return score


print(task1())
print(task2())
