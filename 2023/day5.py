import re
import fileinput
from typing import List, Tuple


MAP_LINE_PATTERN = re.compile(r"^([a-z]+)-to-([a-z]+) map:")


def get_seed_ranges_part_1(nums: List[int]) -> List[Tuple[int, int]]:
    return [(num, num) for num in nums]


def get_seed_ranges_part_2(nums: List[int]) -> List[Tuple[int, int]]:
    out = []
    for start, length in zip(nums[::2], nums[1::2]):
        out.append((start, start + length - 1))
    return out


def main(is_part_1: bool) -> None:
    lines = list(filter(None, map(str.strip, fileinput.input())))

    if is_part_1:
        get_seed_ranges = get_seed_ranges_part_1
    else:
        get_seed_ranges = get_seed_ranges_part_2

    seed_ranges = []
    progression = {}
    maps = {}
    line_idx = 0

    while line_idx < len(lines):
        next_line = lines[line_idx]
        line_idx += 1

        if next_line.startswith("seeds:"):
            _, seed_nums_str = next_line.split(":", 1)
            seed_num_strs = seed_nums_str.strip().split(" ")
            seed_nums = list(map(int, seed_num_strs))
            seed_ranges = get_seed_ranges(seed_nums)
            continue

        match = MAP_LINE_PATTERN.match(next_line)
        if not match:
            raise RuntimeError(f"Unexpected line: {repr(next_line)}")

        from_type = match.group(1)
        to_type = match.group(2)

        progression[from_type] = to_type
        current_map = maps[from_type, to_type] = {}

        while line_idx < len(lines) and lines[line_idx][0].isdigit():
            mapping_num_strs = lines[line_idx].strip().split(" ")
            dest_start, src_start, length = map(int, mapping_num_strs)
            src_range = src_start, src_start + length - 1
            current_map[src_range] = dest_start

            line_idx += 1

    if not seed_ranges:
        raise RuntimeError("seed ranges not found")

    start_type = "seed"
    end_type = "location"

    current_type = start_type
    current_ranges = seed_ranges

    while current_type != end_type:
        dest_type = progression[current_type]
        current_map = maps[current_type, dest_type]

        unmapped_ranges = current_ranges
        next_ranges = []

        for (src_start, src_end), dest_start in current_map.items():
            next_unmapped_ranges = []

            for (current_start, current_end) in unmapped_ranges:
                if current_start > src_end or current_end < src_start:
                    next_unmapped_ranges.append((current_start, current_end))
                    continue

                if current_start < src_start:
                    next_unmapped_ranges.append((current_start, src_start - 1))
                if current_end > src_end:
                    next_unmapped_ranges.append((src_end + 1, current_end))
                
                overlap_start = max(current_start, src_start)
                overlap_end = min(current_end, src_end)
    
                overlap_dest_start = dest_start + overlap_start - src_start
                overlap_dest_end = dest_start + overlap_end - src_start
                if overlap_dest_start <= overlap_dest_end:
                    next_ranges.append((overlap_dest_start, overlap_dest_end))

            unmapped_ranges = next_unmapped_ranges
        
        next_ranges.extend(unmapped_ranges)
        current_ranges = next_ranges
        current_type = dest_type
    
    print("MIN LOCATION", min(start for start, _ in current_ranges))


if __name__ == "__main__":
    # main(is_part_1=True)
    main(is_part_1=False)
