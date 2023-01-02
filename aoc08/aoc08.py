
def get_input() -> list[list[int]]:
    input_lines: list[list[int]] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append([int(char) for char in line.strip()])
    return input_lines


def is_visible(i: int, j: int, grid: list[list[int]]) -> bool:
    height = grid[i][j]
    largest_up = max([grid[y][j] for y in range(i)]+[-1])
    largest_down = max([grid[y][j] for y in range(i+1, len(grid))]+[-1])
    largest_left = max([grid[i][x] for x in range(j)]+[-1])
    largest_right = max([grid[i][x] for x in range(j+1, len(grid[i]))]+[-1])
    return height > largest_up or height > largest_down or height > largest_left or height > largest_right


def scenic_score(i: int, j: int, grid: list[list[int]]) -> int:
    score = 1
    height = grid[i][j]
    distance = 0
    for y in range(i-1, -1, -1):
        distance += 1
        if grid[y][j] >= height:
            break
    score *= distance
    distance = 0
    for y in range(i+1, len(grid)):
        distance += 1
        if grid[y][j] >= height:
            break
    score *= distance
    distance = 0
    for x in range(j-1, -1, -1):
        distance += 1
        if grid[i][x] >= height:
            break
    score *= distance
    distance = 0
    for x in range(j+1, len(grid[i])):
        distance += 1
        if grid[i][x] >= height:
            break
    score *= distance
    return score


grid = [
    [3, 0, 3, 7, 3],
    [2, 5, 5, 1, 2],
    [6, 5, 3, 3, 2],
    [3, 3, 5, 4, 9],
    [3, 5, 3, 9, 0],
]

grid = get_input()


def task1():
    result = 0
    for i, line in enumerate(grid):
        for j, tree in enumerate(line):
            if is_visible(i, j, grid):
                result += 1
    return result


def task2():
    result = 0
    for i, line in enumerate(grid):
        for j, tree in enumerate(line):
            if (score := scenic_score(i, j, grid)) > result:
                result = score
    return result


print(task1())

print(scenic_score(3, 2, grid))
print(task2())
