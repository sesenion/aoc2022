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
class Processor:
    result2: list[str]
    x: int = 1
    cycle: int = 0
    result1: int = 0
    line: str = ""

    def increase_cycle(self):
        raster_pos = self.cycle % 40
        if raster_pos == 0:
            self.result2.append(self.line)
            self.line = ""
        self.cycle += 1
        if abs(raster_pos - self.x) < 2:
            self.line += "#"
        else:
            self.line += "."
        if (self.cycle - 20) % 40 == 0:
            self.result1 += self.cycle * self.x

    def noop(self):
        self.increase_cycle()

    def addx(self, value: int):
        self.increase_cycle()
        self.increase_cycle()
        self.x += value


proc = Processor(result2=[])
for line in get_input():
    match line.split():
        case ["noop"]:
            proc.noop()
        case ["addx", value]:
            proc.addx(int(value))

print(proc.result1)
for line in proc.result2:
    print(line)
print(proc.line)
