from dataclasses import dataclass
from typing import Self

from flask import Flask
import jinja2

J2ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"), autoescape=jinja2.select_autoescape()
)


def get_input(filename: str | None) -> list[str]:
    if filename is None:
        filename = "input.txt"
    input_lines: list[str] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


@dataclass(eq=True, frozen=True)
class Position:
    x: int = 0
    y: int = 0

    @classmethod
    def from_string(cls, input_string: str) -> Self:
        x, y = (int(val) for val in input_string.split(","))
        instance = cls(x=x, y=y)
        return instance


NEW_GRAIN_POSITION = Position(500, 0)


class Cave:
    def __init__(self, min_pos: Position, max_pos: Position) -> None:
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.positions: dict[Position, int] = {}
        self.current_grain: Position = NEW_GRAIN_POSITION
        self.update_counter: int = 0
        self.number_of_grains: int = 1
        self.set(self.current_grain, 2)

    @property
    def min_x(self) -> int:
        return min(pos.x for pos in self.positions.keys())

    @property
    def max_x(self) -> int:
        return max(pos.x for pos in self.positions.keys())

    @property
    def min_y(self) -> int:
        return 0

    @property
    def max_y(self) -> int:
        return max(pos.y for pos in self.positions.keys())

    def get(self, pos: Position) -> int:
        if pos.y > self.max_pos.y + 1:
            return 1
        if not pos in self.positions:
            return 0
        return self.positions[pos]

    def set(self, pos: Position, value: int):
        self.positions[pos] = value

    def draw_rock(self, edges: list[Position]):
        for edge in edges:
            self.set(edge, 1)
        for i in range(len(edges) - 1):
            edge1 = edges[i]
            edge2 = edges[i + 1]
            if edge1.x == edge2.x:
                for y in range(min(edge1.y, edge2.y), max(edge1.y, edge2.y)):
                    self.set(Position(edge1.x, y), 1)
            if edge1.y == edge2.y:
                for x in range(min(edge1.x, edge2.x), max(edge1.x, edge2.x)):
                    self.set(Position(x, edge1.y), 1)

    def paint(self):
        """Creates a matrix of Characters for the HTML output"""
        symbols = {
            0: ".",
            1: "#",
            2: "°",
        }
        output = []
        for y in range(self.min_y, self.max_y + 1):
            line = []
            for x in range(self.min_x, self.max_x + 1):
                line.append(symbols[self.get(Position(x, y))])
            output.append(line)
        return output

    def move_grain(self) -> bool:
        """Tries to move the grain down, bottom-left or bottom-right in that order.

        If it has been moved, return True,
        If no space free in these positions, return False
        """

        below = Position(x=self.current_grain.x, y=self.current_grain.y + 1)
        bottom_left = Position(x=self.current_grain.x - 1, y=self.current_grain.y + 1)
        bottom_right = Position(x=self.current_grain.x + 1, y=self.current_grain.y + 1)
        target: Position
        if self.get(below) == 0:
            target = below
        elif self.get(bottom_left) == 0:
            target = bottom_left
        elif self.get(bottom_right) == 0:
            target = bottom_right
        else:
            return False
        self.set(self.current_grain, 0)
        self.current_grain = target
        self.set(target, 2)
        return True

    def new_grain(self) -> bool:
        """Initializes a new grain if the new grain position is free.
        returns True on success, False on failure

        Returns:
            bool: Operation Performed
        """
        if self.get(NEW_GRAIN_POSITION) != 0:
            return False
        self.number_of_grains += 1
        self.set(NEW_GRAIN_POSITION, 2)
        self.current_grain = NEW_GRAIN_POSITION
        return True

    def update(self) -> bool:
        moved = self.move_grain()
        if not moved:
            new_grain_created = self.new_grain()
            if not new_grain_created:
                return False
        self.update_counter += 1
        return True


def parse_input(input_lines: list[str]) -> list[list[Position]]:
    output = []
    for line in input_lines:
        tuple_strings = line.split("->")
        output.append(
            [Position.from_string(tuple_string) for tuple_string in tuple_strings]
        )
    return output


def get_dimensions(parsed_input: list[list[Position]]) -> tuple[Position, Position]:
    min_x = 100000
    min_y = 0
    max_x = -100000
    max_y = -100000
    for path in parsed_input:
        for position in path:
            min_x = min(min_x, position.x)
            max_x = max(max_x, position.x)
            max_y = max(max_y, position.y)
    return Position(min_x, min_y), Position(max_x, max_y)


input_lines = get_input("input.txt")
parsed_input = parse_input(input_lines)
min_pos, max_pos = get_dimensions(parsed_input)
cave = Cave(min_pos, max_pos)
for line in parsed_input:
    cave.draw_rock(line)

if __name__ == "__main__":
    while True:
        updated = cave.update()
        if cave.update_counter % 100 == 0:
            print(f"grain {cave.number_of_grains} at iteration {cave.update_counter}")
        if cave.current_grain.y > cave.max_pos.y:
            print(
                f"The first grain to fall through is number {cave.number_of_grains} at iteration {cave.update_counter}."
            )
            break

    while True:
        updated = cave.update()
        if cave.update_counter % 100 == 0:
            print(f"grain {cave.number_of_grains} at iteration {cave.update_counter}")
        if not updated:
            print(
                f"The last grain to enter was {cave.number_of_grains} at iteration {cave.update_counter}."
            )
            break


app = Flask(__name__)


@app.route("/")
def index():
    return J2ENV.get_or_select_template("index.html.jinja2").render(
        {"cave": render_cave()}
    )


@app.route("/cave")
def render_cave():
    return J2ENV.get_or_select_template("cave.html.jinja2").render(
        {
            "update_counter": cave.update_counter,
            "number_of_grains": cave.number_of_grains,
            "cave": cave.paint(),
        }
    )


@app.route("/update-cave")
def update_cave():
    cave.update()
    return render_cave()
