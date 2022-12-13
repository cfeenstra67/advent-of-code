import fileinput
import itertools
from functools import cmp_to_key
from typing import Any, Iterator, Tuple


def parse_packet(line: str) -> Any:

    def parse_partial(inp: str) -> (Any, str):
        if inp[0] == "[":
            items = []
            rest = inp[1:]
            while rest[0] != "]":
                next_item, rest = parse_partial(rest)
                items.append(next_item)
                if rest[0] == ",":
                    rest = rest[1:]
                elif rest[0] != "]":
                    raise ValueError(f"Invalid input: {inp}")

            return items, rest[1:]

        if inp[0].isdigit():
            nums = 1
            rest = inp[1:]
            while rest and rest[0].isdigit():
                nums += 1
                rest = rest[1:]
            return int(inp[:nums]), inp[nums:]

        raise ValueError(f"Invalid input: {inp}")

    result, rest = parse_partial(line)
    if rest:
        raise ValueError(f"Unexpected extra input: {rest}")
    return result


def parse_packet_pairs(lines: Iterator[str]) -> Iterator[Tuple[Any, Any]]:
    i = iter(lines)
    while True:
        lines = list(map(next, [i] * 2))
        if len(lines) != 2:
            break

        yield parse_packet(lines[0]), parse_packet(lines[1])


def compare_packets(packet_1: Any, packet_2: Any) -> int:
    is_int_1 = isinstance(packet_1, int)
    is_int_2 = isinstance(packet_2, int)

    if is_int_1 and is_int_2:
        if packet_1 == packet_2:
            return 0
        if packet_1 > packet_2:
            return 1
        return -1

    if not (is_int_1 or is_int_2):
        if len(packet_2) < len(packet_1):
            return -compare_packets(packet_2, packet_1)

        for item_1, item_2 in itertools.zip_longest(packet_1, packet_2):
            if item_1 is None:
                return -1

            comparison_result = compare_packets(item_1, item_2)
            if comparison_result != 0:
                return comparison_result

        return 0

    if is_int_1:
        return compare_packets([packet_1], packet_2)

    return compare_packets(packet_1, [packet_2])


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    # right_order = 0
    # for idx, (packet_1, packet_2) in enumerate(parse_packet_pairs(lines)):
    #     if compare_packets(packet_1, packet_2) == -1:
    #         right_order += idx + 1

    # print("RIGHT", right_order)

    divider_packets = [[[2]], [[6]]]
    packets = list(map(parse_packet, lines))
    packets.extend(divider_packets)
    packets.sort(key=cmp_to_key(compare_packets))

    divider_indexes = []
    divider_product = 1
    for divider in divider_packets:
        idx = packets.index(divider) + 1
        print("DIVIDER", divider, idx)
        divider_product *= idx

    print("PRODUCT", divider_product)


if __name__ == '__main__':
    main()
