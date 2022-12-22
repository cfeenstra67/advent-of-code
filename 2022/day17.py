import fileinput
import itertools
from typing import List, Tuple, Iterable, Optional

ROCK_STRS = [
    "####",

    ".#.\n"
    "###\n"
    ".#.",

    "..#\n"
    "..#\n"
    "###",

    "#\n"
    "#\n"
    "#\n"
    "#",

    "##\n"
    "##"
]


class Rock:

    def __init__(self, points: List[Tuple[int, int]]) -> None:
        self.points = points
        self.max_y = max(y for x, y in points)
        self.max_x = max(x for x, y in points)


class RockSimulation:

    def __init__(
        self,
        width: int,
        gusts_iter: Iterable[bool],
        wall_offset: int,
        floor_offset: int,
    ) -> None:
        self.min_y = 1
        self.width = width
        self.gusts_iter = gusts_iter
        self.points = {}
        self.wall_offset = wall_offset
        self.floor_offset = floor_offset

    def height(self) -> int:
        return -self.min_y + 1

    def top_xs(self) -> List[int]:
        return sorted([x for x, y in self.points if y == self.min_y])

    def drop_rock(self, rock: Rock) -> None:
        initial_y = self.min_y - self.floor_offset - rock.max_y - 1
        initial_x = self.wall_offset

        origin_x, origin_y = initial_x, initial_y

        while True:
            # First it gets blown by a gust of wind
            is_right = next(self.gusts_iter)
            x_offset = 1 if is_right else -1

            new_points = [(origin_x + x + x_offset, origin_y + y) for x, y in rock.points]
            if not any(
                (x, y) in self.points
                or x >= self.width
                or x < 0
                for x, y in new_points
            ):
                origin_x += x_offset

            # Then it falls--if it's reached another rock or
            # the floor, it's done falling
            new_points = [(origin_x + x, origin_y + y + 1) for x, y in rock.points]
            if any(
                (x, y) in self.points
                or y > 0
                for x, y in new_points
            ):
                break

            origin_y += 1

        self.min_y = min(self.min_y, origin_y)
        self.points.update({
            (x + origin_x, y + origin_y): rock for x, y in rock.points
        })

    def grid(self, current: Optional[List[Tuple[int, int]]] = None) -> List[List[int]]:
        if current is None:
            current = []
            min_y = self.min_y
        else:
            min_y = min(self.min_y, min(y for x, y in current))

        current_set = set(current)

        lines = []
        for y in range(min_y, 1):
            line = []
            for x in range(self.width):
                if (x, y) in current_set:
                    line.append(2)
                elif (x, y) in self.points:
                    line.append(1)
                else:
                    line.append(0)
            lines.append(line)

        return lines[::-1]

    def print(self, current: Optional[List[Tuple[int, int]]] = None) -> str:
        grid = self.grid(current)[::-1]

        lines = []
        for grid_line in grid:
            line = ["|"]
            for item in grid_line:
                if item == 0:
                    line.append(".")
                elif item == 1:
                    line.append("#")
                elif item == 2:
                    line.append("@")
                else:
                    raise ValueError(f"Invalid item: {item}")

            line.append("|")
            lines.append("".join(line))

        lines.append("+" + self.width * "-" + "+")
        return "\n".join(lines)


def parse_rock(block_str: str) -> Rock:
    points = []
    for y, line in enumerate(block_str.split("\n")):
        for x, char in enumerate(line):
            if char == ".":
                continue
            points.append((x, y))
    return Rock(points)


def parse_gusts(line: str) -> List[bool]:
    out = []
    for char in line:
        if char == ">":
            out.append(True)
        else:
            out.append(False)
    return out


def find_cycle(gusts: List[bool], rocks: List[Rock]) -> Tuple[int, int]:
    cutoff = 100
    num_rocks = len(rocks) * cutoff
    max_num_rocks = 1_000_000

    while num_rocks < max_num_rocks:
        simulation, heights = run_simulation(num_rocks, gusts, rocks)
        height_diffs = [second - first for first, second in zip(heights, heights[1:])]

        def test(offset, length):
            start_idxs = range(offset, len(height_diffs) - length * 2, length)
            if len(start_idxs) < cutoff:
                return False, 0

            correct = 0
            for start_idx in start_idxs:
                first_chunk = height_diffs[start_idx:start_idx + length]
                second_chunk = height_diffs[start_idx + length:start_idx + length * 2]
                if first_chunk != second_chunk:
                    return False, correct
                correct += 1
            return True, correct

        for offset in range(0, len(heights) // 2, len(rocks)):
            min_cycle_length = offset + len(rocks)
            max_cycle_length = (len(heights) - offset) // cutoff
            for length in range(min_cycle_length, max_cycle_length + 1, len(rocks)):
                first_chunk = height_diffs[offset:offset + length]
                second_chunk = height_diffs[offset + length:offset + length * 2]
                if first_chunk == second_chunk:
                    correct, num_matches = test(offset, length)
                    if not correct or num_matches < cutoff:
                        continue
                    return offset, length

        num_rocks *= 2

    raise ValueError("Cycle not found")


def run_simulation(num_rocks: int, gusts: List[bool], rocks: List[Rock]) -> Tuple[RockSimulation, List[int]]:
    width = 7
    wall_offset = 2
    floor_offset = 3

    rocks_iter = itertools.cycle(rocks)
    gusts_iter = itertools.cycle(gusts)

    simulation = RockSimulation(width, gusts_iter, wall_offset, floor_offset)
    heights = [simulation.height()]

    for idx, rock in enumerate(rocks_iter):
        if idx >= num_rocks:
            break
        simulation.drop_rock(rock)
        heights.append(simulation.height())

    return simulation, heights


def calculate_height(num_rocks: int, gusts: List[bool], rocks: List[Rock]) -> int:
    offset, length = find_cycle(gusts, rocks)
    _, heights = run_simulation(offset + length, gusts, rocks)

    if num_rocks < len(heights):
        return heights[num_rocks]

    offset_height = heights[offset]

    height_diffs = [second - first for first, second in zip(heights, heights[1:])]
    cycle_height = sum(height_diffs[offset:])

    num_full_cycles = (num_rocks - offset) // length
    remainder = (num_rocks - offset) % length

    remainder_height = sum(height_diffs[offset:offset + remainder])
    return offset_height + num_full_cycles * cycle_height + remainder_height


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    gusts = list(itertools.chain.from_iterable(map(parse_gusts, lines)))
    rocks = list(map(parse_rock, ROCK_STRS))

    # num_rocks = 2022
    num_rocks = 1000000000000

    print("HEIGHT", calculate_height(num_rocks, gusts, rocks))


if __name__ == '__main__':
    main()
