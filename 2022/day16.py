import dataclasses as dc
import fileinput
import itertools
from typing import Iterator, Set, List, Dict


@dc.dataclass(frozen=True)
class ValveInfo:
    name: str
    flow_rate: int
    tunnels: Set[str]


def parse_valve(line: str) -> ValveInfo:
    valve_info, downstream = map(str.strip, line.split(";"))
    _, name, _, _, rate_str = valve_info.split()
    _, _, _, _, tunnels_str = downstream.split(None, 4)
    tunnels = list(map(str.strip, tunnels_str.split(",")))
    return ValveInfo(
        name=name,
        flow_rate=int(rate_str.split("=")[1]),
        tunnels=set(tunnels)
    )


def max_pressure_released(
    valves: Dict[str, ValveInfo],
    actors: List[str],
    time_steps: int,
) -> int:
    queue = [
        ({actor: "AA" for actor in actors}, 0, set(), 0, [])
    ]

    best_flow_rates = {}
    max_flowed = 0
    max_steps = None

    while queue:
        current_valves, time_step, opened_valves, flowed, steps = queue.pop(0)
        flow_rate = sum(valves[valve].flow_rate for valve in opened_valves)

        if time_step == time_steps:
            if flowed > max_flowed:
                max_flowed = flowed
                max_steps = steps
            continue

        key = tuple(sorted(current_valves.values()))

        skip = False
        for other_time_step, other_flowed, other_flow_rate in best_flow_rates.get(key, []):
            if (
                other_time_step <= time_step
                and other_flowed >= flowed
                and other_flow_rate >= flow_rate
            ):
                skip = True
                break

        if skip:
            continue

        best_flow_rates.setdefault(key, []).append((time_step, flowed, flow_rate))

        flowed += flow_rate

        if opened_valves == set(valves):
            queue.append((
                current_valves,
                time_step + 1,
                opened_valves,
                flowed,
                steps + [{
                    "moves": {actor: {"type": "none"} for actor in actors},
                    "open": sorted(opened_valves),
                    "flowed": flowed
                }]
            ))
            continue

        possible_moves = {}

        for actor, current_valve in current_valves.items():
            # Optimization: if the _last_ move was `none`, only consider that
            # for the rest of the run--loafing around before the job is done
            # won't get us anywhere!
            possible_moves.setdefault(actor, []).append(("none", None))
            if steps and steps[-1]["moves"][actor]["type"] == "none":
                continue
            # Optimization: don't consider opening valves w/ flow rate of 0, that
            # won't improve our overall flow rate
            if valves[current_valve].flow_rate > 0:
                possible_moves.setdefault(actor, []).append(("open", current_valve))

            for other_valve in valves[current_valve].tunnels:
                possible_moves.setdefault(actor, []).append(("move", other_valve))

        actors, possible_move_lists = zip(*possible_moves.items())

        for moves in itertools.product(*possible_move_lists):
            moves_dict = dict(zip(actors, moves))
            new_opened_values = set(opened_valves)
            new_valves = current_valves.copy()
            step = {}

            skip = False

            for actor, (move_name, move_target) in moves_dict.items():
                step[actor] = {"type": move_name, "target": move_target}
                if move_name == "open" and move_target in new_opened_values:
                    skip = True
                    break
                elif move_name == "open":
                    new_opened_values.add(move_target)
                elif move_name == "move":
                    new_valves[actor] = move_target

            if skip:
                continue

            queue.append((
                new_valves,
                time_step + 1,
                new_opened_values,
                flowed,
                steps + [{
                    "moves": step,
                    "open": sorted(opened_valves),
                    "flowed": flowed,
                }]
            ))

    return max_flowed, max_steps


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    valves_by_name = {valve.name: valve for valve in map(parse_valve, lines)}
    # result, max_steps = max_pressure_released(valves_by_name, ["me"], 30)
    result, max_steps = max_pressure_released(valves_by_name, ["me", "elephant"], 26)

    for idx, step in enumerate(max_steps):
        print("Minute", idx + 1)
        flow_rate = sum(valves_by_name[valve].flow_rate for valve in step["open"])
        if step["open"]:
            print("Valves", ", ".join(step["open"]), "are open, releasing", flow_rate, "pressure")
        else:
            print("No valves are open")
        for actor, move in step["moves"].items():
            if move["type"] == "open":
                print(actor, "opens valve", move["target"])
            elif move["type"] == "move":
                print(actor, "moves to", move["target"])
        print()

    print("RESULT", result)


if __name__ == '__main__':
    main()
