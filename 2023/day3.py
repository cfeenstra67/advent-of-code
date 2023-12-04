import fileinput
import functools
from typing import Dict, Tuple, List


def is_part_number(line_idx: int, start_idx: int, length: int, symbols: Dict[Tuple[int, int], str]) -> bool:
    for check_line_idx in range(line_idx - 1, line_idx + 2):
        for check_char_idx in range(start_idx - 1, start_idx + length + 1):
            if (check_line_idx, check_char_idx) in symbols:
                return True
    return False


def adjacent_parts(line_idx: int, char_idx: int, numbers: Dict[Tuple[int, int], int]) -> List[int]:
    part_ids = set()
    
    for check_line_idx in range(line_idx - 1, line_idx + 2):
        for check_char_idx in range(char_idx - 1, char_idx + 2):
            if (check_line_idx, check_char_idx) in numbers:
                part_ids.add(numbers[check_line_idx, check_char_idx])

    return list(part_ids)


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))

    numbers = {}
    symbols = {}

    for line_idx, line in enumerate(lines):
        number_chars = []
        for char_idx, char in enumerate(line):
            if char.isdigit():
                number_chars.append(char)
                continue
            if number_chars:
                start_idx = char_idx - len(number_chars)
                number_val = int("".join(number_chars))
                numbers[line_idx, start_idx] = number_val, len(number_chars)
                number_chars = []
            if char == ".":
                continue
            symbols[line_idx, char_idx] = char
        
        if number_chars:
            start_idx = len(line) - len(number_chars)
            number_val = int("".join(number_chars))
            numbers[line_idx, start_idx] = number_val, len(number_chars)
    
    total = 0
    for (line_idx, char_idx), (number_val, number_length) in numbers.items():
        if is_part_number(line_idx, char_idx, number_length, symbols):
            total += number_val

    print("TOTAL", total)

    expanded_numbers = {}
    parts_by_id = {}
    for number_id, ((line_idx, start_idx), (number_val, length)) in enumerate(numbers.items()):
        for char_idx in range(start_idx, start_idx + length):
            expanded_numbers[line_idx, char_idx] = number_id
            parts_by_id[number_id] = number_val

    total_gear_ratio = 0
    for (line_idx, char_idx), symbol in symbols.items():
        if symbol != "*":
            continue
        part_ids = adjacent_parts(line_idx, char_idx, expanded_numbers)
        if len(part_ids) != 2:
            continue
        part_numbers = [parts_by_id[part_id] for part_id in part_ids]
        gear_ratio = functools.reduce(lambda x, y: x * y, part_numbers)
        total_gear_ratio += gear_ratio
    
    print("GEAR RATIO TOTAL", total_gear_ratio)


if __name__ == "__main__":
    main()
