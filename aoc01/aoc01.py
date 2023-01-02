from collections import defaultdict


def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


def fill_elves(input_lines: list[str]) -> dict[int, str]:
    elves = defaultdict(list)
    start_line = 0
    for i, line in enumerate(input_lines):
        if not line:
            start_line = i + 1
            continue
        elves[start_line].append(int(line))
    return elves


def task1():
    input_lines = get_input()
    elves = fill_elves(input_lines)
    return max(sum(elf) for elf in elves.values())


def task2():
    input_lines = get_input()
    elves = fill_elves(input_lines)
    backpacks = sorted(list(sum(elf) for elf in elves.values()), reverse=True)
    return sum(backpacks[:3])


print(task1())
print(task2())
