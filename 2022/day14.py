import fileinput
from typing import List, Tuple, Iterator


class CaveSimulation:
    """
    """
    def __init__(self) -> None:
        self.objects = {}
        self.max_y = 0

    def add_lines(self, points: List[Tuple[int, int]]) -> None:
        symbol = "#"

        for (from_x, from_y), (to_x, to_y) in zip(points, points[1:]):
            diff_x = to_x - from_x
            diff_y = to_y - from_y
            if diff_x == 0:
                min_y = min(from_y, to_y)
                max_y = max(from_y, to_y)
                for y in range(min_y, max_y + 1):
                    self.objects[from_x, y] = symbol
            elif diff_y == 0:
                min_x = min(from_x, to_x)
                max_x = max(from_x, to_x)
                for x in range(min_x, max_x + 1):
                    self.objects[x, from_y] = symbol
            else:
                raise ValueError(
                    f"Invalid line: {(from_x, from_y)} -> {(to_x, to_y)}"
                )

            self.max_y = max(self.max_y, to_y)

    def drop_sand(self) -> Tuple[int, int]:
        sand_x, sand_y = 500, 0
        symbol = "o"

        while sand_y < self.max_y + 1:
            new_x, new_y = None, None

            for next_x, next_y in [
                # Down
                (sand_x, sand_y + 1),
                # Left Diagonal
                (sand_x - 1, sand_y + 1),
                # Right Diagonal
                (sand_x + 1, sand_y + 1),
            ]:
                if (next_x, next_y) not in self.objects:
                    new_x, new_y = next_x, next_y
                    break

            if new_x is not None:
                sand_x, sand_y = new_x, new_y
                continue

            break

        self.objects[sand_x, sand_y] = symbol
        return sand_x, sand_y

    def print_objects(self) -> str:
        min_x = float("inf")
        max_x = 0
        min_y = float("inf")
        max_y = 0

        for x, y in self.objects:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        lines = []

        for y in range(min_y - 1, max_y + 2):
            line = []
            for x in range(min_x - 1, max_x + 2):
                line.append(self.objects.get((x, y), "."))
            lines.append("".join(line))

        return "\n".join(lines)


def parse_points(lines: Iterator[str]) -> Iterator[List[Tuple[int, int]]]:
    for line in lines:
        components = list(map(str.strip, line.split("->")))
        points = [tuple(map(int, item.split(","))) for item in components]
        yield points


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))

    simulation = CaveSimulation()
    for points in parse_points(lines):
        simulation.add_lines(points)

    last_point = None
    fallen = 0
    while last_point != (500, 0):
        try:
            last_point = simulation.drop_sand()
        except SandFallsForever:
            break
        else:
            fallen += 1
            # print(f"Sand #{fallen}: {last_point}")

    # print(simulation.print_objects())

    print("Fallen", fallen)


if __name__ == '__main__':
    main()
