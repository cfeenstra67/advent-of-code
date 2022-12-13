import fileinput


class RopeGrid:
    """
    """
    def __init__(self, length: int) -> None:
        self.length = length
        self.positions = tuple((0, 0) for _ in range(length))
        self.history = [self.positions]

    def move(self, direction: str) -> None:
        if direction == "R":
            x, y = 1, 0
        elif direction == "L":
            x, y = -1, 0
        elif direction == "U":
            x, y = 0, 1
        elif direction == "D":
            x, y = 0, -1
        else:
            raise ValueError(f"Invalid direction: {direction}")

        head_x, head_y = self.positions[0]
        head_x += x
        head_y += y

        positions = [(head_x, head_y)]
        for tail_x, tail_y in self.positions[1:]:
            diff_x = head_x - tail_x
            diff_y = head_y - tail_y

            if abs(diff_y) == 2 and abs(diff_x) == 2:
                tail_x += diff_x // 2
                tail_y += diff_y // 2
            elif abs(diff_y) == 2:
                if abs(diff_x) > 0:
                    tail_x += diff_x
                tail_y += diff_y // 2
            elif abs(diff_x) == 2:
                if abs(diff_y) > 0:
                    tail_y += diff_y
                tail_x += diff_x // 2

            positions.append((tail_x, tail_y))

            head_x, head_y = tail_x, tail_y

        self.positions = tuple(positions)
        self.history.append(positions)

    def unique_positions(self, idx: int) -> int:
        positions = [tup[idx] for tup in self.history]
        return len(set(positions))

    def print_history(self, after_directions: int) -> str:
        range_x = 0, 0
        range_y = 0, 0
        for positions in self.history:
            for x, y in positions:
                min_x = min(range_x[0], x)
                max_x = max(range_x[1], x)
                min_y = min(range_y[0], y)
                max_y = max(range_y[1], y)
                range_x = min_x, max_x
                range_y = min_y, max_y

        positions = self.history[after_directions]

        position_indexes = {}
        for idx, position in enumerate(positions):
            if position in position_indexes:
                continue
            if idx == 0:
                position_indexes[position] = "H"
            else:
                position_indexes[position] = str(idx)

        rows = []
        for y in range(range_y[0] - 1, range_y[1] + 1):
            row = []

            for x in range(range_x[0] - 1, range_x[1] + 1):
                if (x, y) in position_indexes:
                    row.append(position_indexes[x, y])
                else:
                    row.append(".")

            rows.append("".join(row))

        return "\n".join(reversed(rows))


def main() -> None:
    rope_lengths = [2, 10]
    grids = [RopeGrid(length) for length in rope_lengths]

    # instructions = 0
    # indexes = [0]

    for line in filter(None, map(str.strip, fileinput.input())):
        direction, count_str = line.split()
        count = int(count_str)
        for _ in range(count):
            for grid in grids:
                grid.move(direction)

        # instructions += count
        # indexes.append(instructions)

    # for grid in grids:
    #     # for index in indexes:
    #     for index in range(instructions + 1):
    #         print(grid.print_history(index))
    #         print()

    for length, grid in zip(rope_lengths, grids):
        print("TAIL", length, grid.unique_positions(length - 1))

    # print("HISTORY", grids[1].history)


if __name__ == '__main__':
    main()
