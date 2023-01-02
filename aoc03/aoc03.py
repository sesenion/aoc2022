

def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


for line in get_input():
    assert len(line) % 2 == 0


def priority(letter: str) -> int:
    letter_code = ord(letter)
    if letter_code > 96:
        return letter_code - 96
    return letter_code - 64 + 26


def task1() -> int:
    result = 0
    lines = get_input()
    for line in lines:
        first, second = line[:len(line)//2], line[len(line)//2:]
        first_set, second_set = set(first), set(second)
        overlap = first_set & second_set
        assert len(overlap) == 1
        result += priority(overlap.pop())
    return result


def task2() -> int:
    result = 0
    lines = get_input()
    for i in range(0, len(lines), 3):
        first = set(lines[i])
        second = set(lines[i+1])
        third = set(lines[i+2])
        overlap = first & second & third
        assert len(overlap) == 1
        result += priority(overlap.pop())
    return result


print(task1())
print(task2())
