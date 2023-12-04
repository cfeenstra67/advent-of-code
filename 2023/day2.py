import fileinput
import functools
from typing import Dict, List, Tuple


def parse_line(line: str) -> Tuple[int, List[Dict[str, int]]]:
    prefix, data = line.split(": ", 1)
    game_id = int(prefix.split(" ", 1)[1])
    item_data = data.split("; ")
    items = []
    for item in item_data:
        sub_items = item.split(", ")
        out = {}
        for sub_item in sub_items:
            num, color = sub_item.split(" ", 1)
            out[color] = int(num)
        items.append(out)
    
    return game_id, items


def is_possible(comparison: Dict[str, int], instance: Dict[str, int]) -> bool:
    comparison_colors = set(comparison)
    instance_colors = set(instance)
    if instance_colors - comparison_colors:
        return False
    for color, count in comparison.items():
        if color not in instance:
            continue
        if count < instance[color]:
            return False
    return True


def fewest_total_cubes(instances: List[Dict[str, int]]) -> Dict[str, int]:
    out = {}
    for instance in instances:
        for key, value in instance.items():
            if key in out:
                out[key] = max(out[key], value)
            else:
                out[key] = value
    return out


def cubes_power(cubes: Dict[str, int]) -> int:
    values = [
        cubes.get(color, 0)
        for color in ["red", "green", "blue"]
    ]
    if len(values) == 0:
        return 0

    return functools.reduce(lambda x, y: x * y, values)


def main() -> None:
    total = 0
    total_power = 0
    comparison = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    lines = filter(None, map(str.strip, fileinput.input()))
    for game_id, instances in map(parse_line, lines):
        fewest_cubes = fewest_total_cubes(instances)
        power = cubes_power(fewest_cubes)
        total_power += power

        if all(is_possible(comparison, instance) for instance in instances):
            total += game_id
    
    print("TOTAL", total)
    print("TOTAL POWER", total_power)


if __name__ == "__main__":
    main()
