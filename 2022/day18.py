import fileinput
import itertools
import operator
from typing import Tuple, Set, Callable


def parse_point(line: str) -> Tuple[int, int, int]:
    return tuple(map(int, line.split(",")))


def adjacencies(point: Tuple[int, int, int]) -> Set[Tuple[int, int, int]]:
    x, y, z = point
    return {
        (x, y - 1, z),
        (x, y + 1, z),
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y, z - 1),
        (x, y, z + 1)
    }


def is_in_range(points: Set[Tuple[int, int, int]]) -> Callable[[Tuple[int, int, int]], bool]:
    xs = list(map(operator.itemgetter(0), points))
    ys = list(map(operator.itemgetter(1), points))
    zs = list(map(operator.itemgetter(2), points))
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    def func(point):
        x, y, z = point
        range_tuples = [
            (x, range(min_x - 1, max_x + 2)),
            (y, range(min_y - 1, max_y + 2)),
            (z, range(min_z - 1, max_z + 2)),
        ]
        return all(
            coordinate in coordinate_range
            for coordinate, coordinate_range in range_tuples
        )

    return func


def is_air_bubble(point: Tuple[int, int, int], points: Set[Tuple[int, int, int]]) -> bool:

    ignore_points = set()

    is_valid_point = is_in_range(points)

    def is_air_bubble_inner(current_point: Tuple[int, int, int]):
        ignore_points.add(current_point)
        for other_point in adjacencies(current_point):
            if other_point in ignore_points:
                continue
            if not is_valid_point(other_point):
                return False
            if not (other_point in points or is_air_bubble_inner(other_point)):
                return False
        return True

    return is_air_bubble_inner(point)


def surface_area(points: Set[Tuple[int, int, int]]) -> int:
    total = 0

    empty_points = []

    for x, y, z in points:
        blockers = adjacencies((x, y, z))
        for point in blockers:
            if point not in points and not is_air_bubble(point, points):
                empty_points.append(point)

    return len(empty_points)


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    points = set(map(parse_point, lines))
    print("AREA", surface_area(points))


if __name__ == '__main__':
    main()
