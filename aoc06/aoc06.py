
def get_input() -> list[str]:
    input_lines: list[str] = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            input_lines.append(line.strip())
    return input_lines


def is_marker(stream: str, position: int, length: int) -> bool:
    """Shows if the 4 characters at a given positon are a marker, 
    meaning all different

    Args:
        stream (str): the data stream
        position (int): position in the data stream

    Returns:
        bool: marker or not
    """
    if position > len(stream) - length:
        return False
    return len(set(stream[position:position+length])) == length


def task1():
    stream = get_input()[0]
    length = 4
    for i in range(len(stream)):
        if is_marker(stream, i, length):
            return i + length


def task2():
    stream = get_input()[0]
    length = 14
    for i in range(len(stream)):
        if is_marker(stream, i, length):
            return i + length


print(task1())
print(task2())
