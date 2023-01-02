from collections import deque, defaultdict
from dataclasses import dataclass
import re


COMMAND_PATTERN = re.compile(R"^move (\d+) from (\d+) to (\d+)$")


@dataclass
class Command:
    amount: int
    source: int
    target: int


def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


def get_stacks(input_lines: list[str]) -> dict[int, list]:
    stacks: dict[int, deque] = defaultdict(deque)
    for line in input_lines:
        if not "[" in line:
            break
        for i, char in enumerate(line):
            if not char.isalpha():
                continue
            stack_index = (i-1) // 4 + 1
            stacks[stack_index].appendleft(char)
    stacks = {key: list(value) for key, value in stacks.items()}
    return stacks


def parse_command(line: str) -> Command | None:
    if match := re.match(COMMAND_PATTERN, line):
        return Command(*(int(group) for group in match.groups()))
    return None


def move1(stacks: dict[int, list], command: Command):
    for i in range(command.amount):
        stacks[command.target].append(stacks[command.source].pop())


def move2(stacks: dict[int, list], command: Command):
    crates_to_move = stacks[command.source][-command.amount:]
    stacks[command.target].extend(crates_to_move)
    stacks[command.source] = stacks[command.source][:-command.amount]


def task1() -> str:
    input_lines = get_input()
    stacks = get_stacks(input_lines)
    for line in input_lines:
        command = parse_command(line)
        if not command:
            continue
        move1(stacks, command)
    return "".join(stacks[key][-1] for key in sorted(stacks))


def task2() -> str:
    input_lines = get_input()
    stacks = get_stacks(input_lines)
    for line in input_lines:
        command = parse_command(line)
        if not command:
            continue
        move2(stacks, command)
    return "".join(stacks[key][-1] for key in sorted(stacks))


print(task1())
print(task2())
