from aoc14 import get_input, Position, parse_input, get_dimensions, Cave


def test_create_position():
    position = Position.from_string("59, 10")
    assert position.x == 59
    assert position.y == 10


def test_parse_input():
    input_lines = get_input("test_input.txt")
    parsed_input = parse_input(input_lines)
    assert len(parsed_input[0]) == 3
    assert parsed_input[1][2].x == 502


def test_get_dimensions():
    input_lines = get_input("test_input.txt")
    parsed_input = parse_input(input_lines)
    min_pos, max_pos = get_dimensions(parsed_input)
    assert min_pos.x == 494
    assert min_pos.y == 0
    assert max_pos.x == 503
    assert max_pos.y == 9


TEST_PIC = """..........
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########.
"""


def test_draw_matrix():
    input_lines = get_input("test_input.txt")
    parsed_input = parse_input(input_lines)
    min_pos, max_pos = get_dimensions(parsed_input)
    cave = Cave(min_pos, max_pos)
    for line in parsed_input:
        cave.draw_rock(line)
    pic = cave.paint()
    assert pic == TEST_PIC
