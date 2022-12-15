import fileinput
from typing import Tuple, Iterator, Optional


class BeaconMap:

    def __init__(
        self,
        min_x: Optional[float] = None,
        max_x: Optional[float] = None,
        min_y: Optional[float] = None,
        max_y: Optional[float] = None,
    ) -> None:
        if min_x is None:
            self.min_x = float("inf")
            self.min_x_dynamic = True
        else:
            self.min_x = min_x
            self.min_x_dynamic = False

        if max_x is None:
            self.max_x = -float("inf")
            self.max_x_dynamic = True
        else:
            self.max_x = max_x
            self.max_x_dynamic = False

        if min_y is None:
            self.min_y = float("inf")
            self.min_y_dynamic = True
        else:
            self.min_y = min_y
            self.min_y_dynamic = False

        if max_y is None:
            self.max_y = -float("inf")
            self.max_y_dynamic = True
        else:
            self.max_y = max_y
            self.max_y_dynamic = False

        self.sensors = {}
        self.beacons = set()

    def add_observation(
        self,
        sensor_x: int,
        sensor_y: int,
        beacon_x: int,
        beacon_y: int,
    ) -> None:
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        if self.min_x_dynamic:
            self.min_x = min(self.min_x, sensor_x - distance)
        if self.max_x_dynamic:
            self.max_x = max(self.max_x, sensor_x + distance)
        if self.min_y_dynamic:
            self.min_y = min(self.min_y, sensor_y - distance)
        if self.max_y_dynamic:
            self.max_y = max(self.max_y, sensor_y + distance)
        self.sensors[sensor_x, sensor_y] = distance
        self.beacons.add((beacon_x, beacon_y))

    # def _get_row(self, y: int) -> Iterator[str]:
    #     ranges = []
    #     for (sensor_x, sensor_y), distance in self.sensors.items():
    #         y_diff = abs(y - sensor_y)
    #         if y_diff > distance:
    #             continue

    #         x_radius = distance - y_diff
    #         ranges.append((
    #             max(self.min_x, sensor_x - x_radius),
    #             min(self.max_x + 1, sensor_x + x_radius + 1)
    #         ))

    #     ranges.sort()

    #     current_x = self.min_x
    #     for (x_start, x_end) in ranges:
    #         for x in range(current_x, x_start):
    #             if (x, y) in self.sensors:
    #                 yield "S"
    #             elif (x, y) in self.beacons:
    #                 yield "B"
    #             else:
    #                 yield "."

    #         for x in range(max(x_start, current_x), x_end):
    #             if (x, y) in self.sensors:
    #                 yield "S"
    #             elif (x, y) in self.beacons:
    #                 yield "B"
    #             else:
    #                 yield "#"

    #         current_x = max(current_x, x_end)

    #     for x in range(current_x, self.max_x + 1):
    #         if (x, y) in self.sensors:
    #             yield "S"
    #         elif (x, y) in self.beacons:
    #             yield "B"
    #         else:
    #             yield "."

    def _candidate_ranges(self, y: int) -> Iterator[str]:
        ranges = []
        for (sensor_x, sensor_y), distance in self.sensors.items():
            y_diff = abs(y - sensor_y)
            if y_diff > distance:
                continue

            x_radius = distance - y_diff
            ranges.append((
                max(self.min_x, sensor_x - x_radius),
                min(self.max_x + 1, sensor_x + x_radius + 1)
            ))

        ranges.sort()

        current_start, current_end = ranges[0]
        merged_ranges = []

        for start_x, end_x in ranges[1:]:
            if start_x > current_end:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start_x, end_x
            else:
                current_end = max(end_x, current_end)

        merged_ranges.append((current_start, current_end))

        if merged_ranges == [(self.min_x, self.max_x + 1)]:
            return []

        left_iter = [self.min_x] + [end for start, end in merged_ranges]
        right_iter = [start for start, end in merged_ranges] + [self.max_x + 1]
        out = []
        for start, end in zip(left_iter, right_iter):
            if start < end:
                out.append((start, end))

        return out

    def print_objects(self) -> str:
        lines = []

        for y in range(self.min_y, self.max_y + 1):
            candidate_ranges = self._candidate_ranges(y)
            candidate_x = set()
            for start_x, end_x in candidate_ranges:
                for x in range(start_x, end_x):
                    candidate_x.add(x)

            line = []
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.beacons:
                    line.append("B")
                elif (x, y) in self.sensors:
                    line.append("S")
                elif x in candidate_x:
                    line.append(".")
                else:
                    line.append("#")

            lines.append("".join(line))

        return "\n".join(lines)

    def number_of_positions_without_a_beacon(self, y: int) -> int:
        total = 0
        for item in self._get_row(y):
            if item in {"#", "S"}:
                total += 1
        return total

    def position_of_beacon(self) -> Tuple[int, int]:
        positions = []
        for y in range(self.min_y, self.max_y + 1):
            candidate_ranges = self._candidate_ranges(y)
            for start_x, end_x in candidate_ranges:
                for x in range(start_x, end_x):
                    if (x, y) not in self.beacons and (x, y) not in self.sensors:
                        positions.append((x, y))

        if len(positions) > 1:
            raise ValueError(f"Multiple beacon positions: {positions}")
        if not positions:
            raise ValueError("Beacon not found")
        return positions[0]


def parse_sensor_data(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    sensor_part, beacon_part = line.split(":")
    _, _, sensor_x_str, sensor_y_str = sensor_part.strip().split()
    _, _, _, _, beacon_x_str, beacon_y_str = beacon_part.strip().split()
    return (
        (int(sensor_x_str[:-1].split("=")[1]), int(sensor_y_str.split("=")[1])),
        (int(beacon_x_str[:-1].split("=")[1]), int(beacon_y_str.split("=")[1])),
    )


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    sensor_data = map(parse_sensor_data, lines)

    # beacon_map = BeaconMap(0, 20, 0, 20)
    beacon_map = BeaconMap(0, 4000000, 0, 4000000)

    for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensor_data:
        beacon_map.add_observation(sensor_x, sensor_y, beacon_x, beacon_y)
        print("ADDED", (sensor_x, sensor_y), (beacon_x, beacon_y))

    # print("OBJECTS")
    # print(beacon_map.print_objects())
    # print()
    # print("POSITIONS", beacon_map.number_of_positions_without_a_beacon(10))
    # print("POSITIONS", beacon_map.number_of_positions_without_a_beacon(2000000))
    x, y = beacon_map.position_of_beacon()
    print("BEACON", (x, y))
    print("FREQUENCY", x * 4000000 + y)


if __name__ == '__main__':
    main()
