import fileinput
from typing import Iterator


def parse_table(lines: Iterator[str]):
    columns = []
    column_labels = []

    index_line = None

    for idx, line in enumerate(lines):
        if not line.strip():
            continue

        # This indicates that it's the index row
        if line.strip()[0] != "[":
            column_labels = line.strip().split()
            break

        col_length = 3

        rest = line
        col_idx = 0
        while rest:
            if idx == 0:
                columns.append([])

            chunk, rest = rest[:col_length], rest[col_length + 1:]
            if chunk[0] == "[":
                columns[col_idx].append(chunk[1])

            col_idx += 1

    return {
        label: list(filter(lambda x: x is not None, col))[::-1]
        for label, col in zip(column_labels, columns)
    }


def handle_instruction_9000(line, table):
    _, count_str, _, src, _, dest = line.split()
    count = int(count_str)
    for _ in range(count):
        item = table[src].pop()
        table[dest].append(item)


def handle_instruction_9001(line, table):
    _, count_str, _, src, _, dest = line.split()
    count = int(count_str)

    tmp = []
    for _ in range(count):
        item = table[src].pop()
        tmp.append(item)

    while tmp:
        table[dest].append(tmp.pop())


def print_top_crates(table):
    for key, column in table.items():
        print("COL", key, column[-1] if column else "<none>")

    print("".join(table[str(i + 1)][-1] for i in range(len(table))))


def main():
    lines = fileinput.input()
    lines = map(lambda x: x.rstrip("\r\n"), lines)

    table = parse_table(lines)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # handle_instruction_9000(line, table)
        handle_instruction_9001(line, table)

    print_top_crates(table)


if __name__ == '__main__':
    main()
