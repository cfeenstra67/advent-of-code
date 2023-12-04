import fileinput
from typing import Tuple, List


def parse_line(line: str) -> Tuple[List[int], List[int]]:
    _, content = line.split(": ", 1)
    winning_numbers_str, has_numbers_str = content.split(" | ", 1)
    winning_numbers = list(map(int, filter(None, winning_numbers_str.split(" "))))
    has_numbers = list(map(int, filter(None, has_numbers_str.split(" "))))
    return winning_numbers, has_numbers


def main() -> None:
    lines = list(filter(None, map(str.strip, fileinput.input())))
    copies = [1 for _ in range(len(lines))]

    total = 0
    for idx, (winning_numbers, has_numbers) in enumerate(map(parse_line, lines)):
        winning_numbers_set = set(winning_numbers)
        count = sum(1 for num in has_numbers if num in winning_numbers_set)
        num_copies = copies[idx]
        for next_idx in range(idx + 1, idx + count + 1):
            copies[next_idx] += num_copies

        if count == 0:
            continue

        points = 2 ** (count - 1)
        total += points
    
    print("TOTAL", total)
    print("TOTAL COPIES", sum(copies))
    

if __name__ == "__main__":
    main()
