from typing import Self, Any
from pathlib import PurePosixPath as Path

from dataclasses import dataclass


def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


@dataclass
class File:
    name: str
    size: int
    parent: Any


@dataclass
class Directory:
    name: str
    parent: Self | None
    children: list[Self | File]

    @property
    def size(self) -> int:
        return sum(child.size for child in self.children)


def build_tree(input_lines: list[str]) -> dict[Path, Directory]:
    dirs = {Path("/"): Directory("/", None, [])}
    current_path: Path = Path("/")
    for line in input_lines:
        match line.split():
            case ["$", "ls"]:
                continue
            case ["$", "cd", "/"]:
                current_path = Path("/")
            case ["$", "cd", ".."]:
                current_path = current_path.parent
            case ["$", "cd", name]:
                current_path = current_path / name
            case ["dir", name]:
                path = (current_path / name).as_posix()
                dirs[current_path].children.append(
                    dir := Directory(path, parent=dirs[current_path], children=[])
                )
                dirs[current_path/name] = dir
            case [number, name]:
                path = (current_path / name).as_posix()
                size = int(number)
                dirs[current_path].children.append(
                    File(path, size, parent=dirs[current_path])
                )
    return dirs


dirs = build_tree(get_input())


def task1():
    return sum(dir.size for dir in dirs.values() if dir.size <= 100000)


def task2():
    total = 70_000_000
    required = 30_000_000
    free = total - dirs[Path("/")].size
    large_enough_dirs = sorted([dir for dir in dirs.values(
    ) if dir.size + free >= required], key=lambda x: x.size)
    return large_enough_dirs[0].size


print(task1())
print(task2())
