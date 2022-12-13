import fileinput
import math
from typing import Iterator, List


def parse_grid(lines: Iterator[str]) -> List[List[int]]:
    grid = []
    for idx, line in enumerate(lines):
        grid.append(list(map(int, line)))
    return grid


def number_visible_from_outside(grid: List[List[int]]) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])

    make_grid = lambda: [[-1 for _ in range(num_cols)] for _ in range(num_rows)]

    left_maxes = make_grid()
    right_maxes = make_grid()
    top_maxes = make_grid()
    bottom_maxes = make_grid()

    for row_idx, row in enumerate(grid):
        left_max = -1
        for col_idx, value in enumerate(row):
            left_maxes[row_idx][col_idx] = left_max
            if value > left_max:
                left_max = value

        right_max = -1
        for col_idx, value in enumerate(reversed(row)):
            real_col_idx = num_cols - col_idx - 1
            right_maxes[row_idx][real_col_idx] = right_max
            if value > right_max:
                right_max = value

    for col_idx in range(num_cols):
        col = [row[col_idx] for row in grid]
        top_max = -1
        for row_idx, value in enumerate(col):
            top_maxes[row_idx][col_idx] = top_max
            if value > top_max:
                top_max = value

        bottom_max = -1
        for row_idx, value in enumerate(reversed(col)):
            real_row_idx = num_rows - row_idx - 1
            bottom_maxes[real_row_idx][col_idx] = bottom_max
            if value > bottom_max:
                bottom_max = value

    num_visible = 0

    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            for name, max_grid in [
                ("left", left_maxes),
                ("right", right_maxes),
                ("top", top_maxes),
                ("bottom", bottom_maxes),
            ]:
                if value <= max_grid[row_idx][col_idx]:
                    continue

                # print("VISIBLE", row_idx, col_idx, name, value, max_grid[row_idx][col_idx])
                num_visible += 1
                break

    return num_visible


def highest_scenic_score(grid: List[List[int]]) -> int:
    max_score = 0

    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            top_visible = 0
            for current_row_idx in range(row_idx - 1, -1, -1):
                top_visible += 1
                other_value = grid[current_row_idx][col_idx]
                if other_value >= value:
                    break

            bottom_visible = 0
            for current_row_idx in range(row_idx + 1, len(grid)):
                bottom_visible += 1
                other_value = grid[current_row_idx][col_idx]
                if other_value >= value:
                    break

            left_visible = 0
            for current_col_idx in range(col_idx - 1, -1, -1):
                left_visible += 1
                other_value = grid[row_idx][current_col_idx]
                if other_value >= value:
                    break

            right_visible = 0
            for current_col_idx in range(col_idx + 1, len(row)):
                right_visible += 1
                other_value = grid[row_idx][current_col_idx]
                if other_value >= value:
                    break

            score = top_visible * bottom_visible * left_visible * right_visible
            if score > max_score:
                max_score = score

    return max_score


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    grid = parse_grid(lines)
    # print("GRID", grid)
    print("VISIBLE", number_visible_from_outside(grid))
    print("SCENIC SCORE", highest_scenic_score(grid))


if __name__ == '__main__':
    main()
