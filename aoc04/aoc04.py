
def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


def get_ranges(line: str) -> tuple[set[int], set[int]]:
    def1, def2 = line.split(",")
    def1, def2 = (d.split("-") for d in (def1, def2))
    range1 = set(range(int(def1[0]), int(def1[1])+1))
    range2 = set(range(int(def2[0]), int(def2[1])+1))
    return range1, range2


def task1() -> int:
    result = 0
    for line in get_input():
        range1, range2 = get_ranges(line)
        overlap = range1.intersection(range2)
        if overlap == range1 or overlap == range2:
            result += 1
    return result


def task2() -> int:
    result = 0
    for line in get_input():
        range1, range2 = get_ranges(line)
        overlap = range1.intersection(range2)
        if overlap:
            result += 1
    return result


print(task1())
print(task2())
