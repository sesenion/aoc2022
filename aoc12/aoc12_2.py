from dataclasses import dataclass
from typing import Self


def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


class Node:
    map: dict[tuple[int, int], Self] = {}
    start_position: tuple[int, int] = (0, 0)
    end_position: tuple[int, int] = (0, 0)
    dimensions: tuple[int, int] = (0, 0)

    @classmethod
    def clear_map(cls):
        cls.map = {}

    @classmethod
    def register_map(cls, input_lines: list[list[str]]):
        x = 0
        y = 0
        for y, line in enumerate(input_lines):
            for x, letter in enumerate(line):
                cls.map[(x, y)] = cls(x, y, letter)
        cls.dimensions = (x + 1, y + 1)
        for node in cls.map.values():
            node.register_neighbors()

    def __init__(self, x: int, y: int, letter: str):
        self.x: int = x
        self.y: int = y
        self.predecessor: Node | None = None
        self.distance_to_start: int = 999999999
        self.processed: bool = False
        self.value: int
        self.edges: list[tuple[int, Self]] = []
        if letter == "S":
            Node.start_position = (x, y)
            self.value = 1
            self.distance_to_start = 0
        elif letter == "E":
            Node.end_position = (x, y)
            self.value = 26
        else:
            self.value = ord(letter) - 96

    def try_register_neighbor(self, x: int, y: int):
        if neighbor := self.map.get((x, y), None):
            edge_cost = neighbor.value - self.value
            if edge_cost < 0:
                edge_cost = 0
            if neighbor.value in (0, 99) or self.value in (0, 99):
                edge_cost = 0
            if edge_cost <= 1:
                self.edges.append((1, neighbor))

    def register_neighbors(self):
        self.try_register_neighbor(self.x, self.y - 1)
        self.try_register_neighbor(self.x, self.y + 1)
        self.try_register_neighbor(self.x - 1, self.y)
        self.try_register_neighbor(self.x + 1, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) Value {self.value}, dist {self.distance_to_start}"


def dijkstra(
    graph: dict[tuple[int, int], Node],
    start_position: tuple[int, int],
):
    start_node: Node = graph[*start_position]
    start_node.distance_to_start = 0
    queue: list[Node] = [
        start_node,
    ]
    counter = 0
    while queue:
        counter += 1
        node_to_process = min(queue, key=lambda node: node.distance_to_start)
        queue.remove(node_to_process)
        for edge_cost, edge_node in sorted(node_to_process.edges, key=lambda x: x[0]):
            if edge_node.processed:
                continue
            new_cost = node_to_process.distance_to_start + edge_cost
            if edge_node in queue and edge_node.distance_to_start <= new_cost:
                continue
            edge_node.distance_to_start = new_cost
            if edge_node not in queue:
                edge_node.predecessor = node_to_process
                queue.append(edge_node)
        node_to_process.processed = True


input_lines = get_input()
Node.register_map(input_lines)
dijkstra(Node.map, Node.start_position)
result1 = Node.map[*Node.end_position].distance_to_start
print(f"Result 1 is {result1}")


Node.clear_map()
Node.register_map(input_lines)
possible_positions: list[tuple[int, int]] = []
for (x, y), node in Node.map.items():
    if node.value == 1:
        possible_positions.append((x, y))

# Extremely ugly and slow, but I am too lazy right now to
# reverse the whole graph logic.
result2 = 99999999
for i, position in enumerate(possible_positions):
    Node.clear_map()
    Node.register_map(input_lines)
    dijkstra(Node.map, position)
    result2 = min(result2, Node.map[*Node.end_position].distance_to_start)

print(f"Result 2 is {result2}")
