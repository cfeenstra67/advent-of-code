import dataclasses as dc
import fileinput
import heapq
from typing import Iterator, List, Tuple


@dc.dataclass(frozen=True)
class MountainMap:
    start_position: Tuple[int, int]
    end_position: Tuple[int, int]
    map: List[List[int]]
    width: int
    height: int

    def print(self) -> str:
        lines = []
        for row_idx, row in enumerate(self.map):
            items = []
            for col_idx, item in enumerate(row):
                if (row_idx, col_idx) == self.start_position:
                    items.append("S")
                elif (row_idx, col_idx) == self.end_position:
                    items.append("E")
                else:
                    items.append(chr(ord('a') + item))
            lines.append("".join(items))
        return "\n".join(lines)


def parse_map(lines: Iterator[str]) -> MountainMap:
    rows = []
    start_position = None
    end_position = None

    letter_index = lambda x: ord(x) - ord('a')

    for row_idx, line in enumerate(lines):
        indexes = []
        for col_idx, char in enumerate(line.strip()):
            if char == "S":
                start_position = row_idx, col_idx
                indexes.append(letter_index('a'))
            elif char == "E":
                end_position = row_idx, col_idx
                indexes.append(letter_index('z'))
            else:
                indexes.append(letter_index(char))

        rows.append(indexes)

    return MountainMap(
        start_position,
        end_position,
        rows,
        len(rows[0]),
        len(rows),
    )


def find_shortest_path(mountain_map: MountainMap) -> int:

    def moves_from_end(row, col):
        end_row, end_col = mountain_map.end_position
        return abs(row - end_row) + abs(col - end_col)

    start_moves = moves_from_end(*mountain_map.start_position)
    queue = [(start_moves, 0, 0, mountain_map.start_position)]

    best_paths = {}

    best_solution = None

    while queue:
        _, _, steps, (row, col) = heapq.heappop(queue)
        if best_solution is not None and steps >= best_solution:
            continue

        if (row, col) == mountain_map.end_position:
            best_solution = steps
            continue

        current_height = mountain_map.map[row][col]

        for diff_row, diff_col in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]:
            new_row = row + diff_row
            new_col = col + diff_col
            if (
                new_row < 0 or new_row >= mountain_map.height
                or new_col < 0 or new_col >= mountain_map.width
            ):
                continue

            move_height = mountain_map.map[new_row][new_col]
            if move_height > current_height + 1:
                continue

            if (
                (new_row, new_col) in best_paths
                and best_paths[new_row, new_col] <= steps + 1
            ):
                continue

            moves = moves_from_end(new_row, new_col)
            heapq.heappush(
                queue,
                (moves, -move_height, steps + 1, (new_row, new_col))
            )
            best_paths[new_row, new_col] = steps + 1

    if best_solution is None:
        raise ValueError("No path found")

    return best_solution


def find_start_positions(mountain_map: MountainMap) -> List[Tuple[int, int]]:
    for row_idx, row in enumerate(mountain_map.map):
        for col_idx, item in enumerate(row):
            if item == 0:
                yield row_idx, col_idx


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    mountain_map = parse_map(lines)
    print("MAP")
    print(mountain_map.print())
    print()
    print("PATH", find_shortest_path(mountain_map))

    shortest = float('inf')

    for row_idx, col_idx in find_start_positions(mountain_map):
        map_with_start_pos = dc.replace(
            mountain_map,
            start_position=(row_idx, col_idx),
        )
        try:
            path_length = find_shortest_path(map_with_start_pos)
        except ValueError:
            print("No path:", (row_idx, col_idx))
            continue
        print("START", (row_idx, col_idx), path_length)
        if path_length < shortest:
            shortest = path_length

    print("SHORTEST", shortest)


if __name__ == '__main__':
    main()
