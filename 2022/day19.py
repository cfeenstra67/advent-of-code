import dataclasses as dc
import fileinput
import heapq
import itertools
import re
from typing import Dict, Any


RESOURCE_TYPES = ["geode", "obsidian", "clay", "ore"]


@dc.dataclass(frozen=True)
class Blueprint:
    id: int
    costs: Dict[str, Dict[str, int]]


def parse_blueprint(line: str) -> Blueprint:
    blueprint_str, costs = line.split(":", 1)
    _, blueprint_id_str = blueprint_str.split()
    blueprint_id = int(blueprint_id_str)

    cost_lines = costs.strip().split(".")[:-1]
    out_costs = {}
    for cost_line in cost_lines:
        result = re.search(r"each (\w+) robot costs (.+)", cost_line, re.I)
        if not result:
            raise ValueError(f"Invalid line: {line}")
        robot_type, costs = result.groups()
        costs_dict = {}
        for item in costs.split(" and "):
            amount, resource_type = item.strip().split()
            costs_dict[resource_type] = int(amount)

        out_costs[robot_type] = costs_dict

    return Blueprint(blueprint_id, out_costs)


def heappush(data, item, key):


    s = list(map(cmp_to_key(cmp), data))
    heapify(s)
    return s

def new_heappop(data):
    return heappop(data).obj


def get_best_number_of_geodes(blueprint: Blueprint, minutes: int) -> Dict[str, Any]:

    def current_potential_geodes(state):
        remaining_minutes = minutes - state["minute"]
        future_geodes = state["robots"].get("geode", 0) * remaining_minutes
        return state["resources"].get("geode", 0) + future_geodes

    # Max potential geodes if we were to create a new geode robot every minute
    # for the rest of the remaining time
    def max_potential_geodes(state):
        remaining_minutes = minutes - state["minute"]
        potential_geodes = remaining_minutes * (remaining_minutes + 1) // 2
        return current_potential_geodes(state) + potential_geodes

    def robots_index(state):
        return sum(
            (len(RESOURCE_TYPES) - RESOURCE_TYPES.index(robot)) ** 2 * count
            for robot, count in state["robots"].items()
        )

    # Force sort key to be unique for all items
    state_index = 0

    def sort_key(item):
        nonlocal state_index
        result = (
            # item["minute"],
            -current_potential_geodes(item),
            -max_potential_geodes(item),
            -robots_index(item),
            state_index,
        )
        state_index += 1
        return result

    initial_state = {
        "robots": {"ore": 1},
        "resources": {},
        "minute": 0,
        "moves": []
    }

    queue = [(sort_key(initial_state), initial_state)]

    best_state = None
    best_num_geodes = -1

    best_states_by_minute = {}

    while queue:
        _, state = heapq.heappop(queue)

        if state["minute"] == minutes:
            if state["resources"].get("geode", 0) > best_num_geodes:
                best_state = state
                best_num_geodes = state["resources"].get("geode", 0)
            continue

        skip = False
        current_max = max_potential_geodes(state)

        for other_state in best_states_by_minute.get(state["minute"], []):
            if all(
                other_state["resources"].get(typ, 0) >= state["resources"].get(typ, 0)
                and other_state["robots"].get(typ, 0) >= state["robots"].get(typ, 0)
                for typ in RESOURCE_TYPES
            ):
                skip = True
                break
            if max_potential_geodes(other_state) > current_max:
                skip = True
                break

        if skip:
            continue

        # for other_minutes, other_states in best_states_by_minute.items():
        #     if other_minutes <= state["minute"]:
        #         continue
        #     for other_state in other_states:
        #         if max_potential_geodes(other_state) > current_max:
        #             skip = True
        #             break
        #     if skip:
        #         break

        # if skip:
        #     continue

        best_states_by_minute.setdefault(state["minute"], []).append(state)

        # Each minute:
        # - each robot collects 1 of its resource type
        # - we can make at most 1 new robot
        new_resources = state["resources"].copy()

        for resource_type, count in state["robots"].items():
            new_resources.setdefault(resource_type, 0)
            new_resources[resource_type] += count

        for robot_type in RESOURCE_TYPES:
            costs = blueprint.costs[robot_type]
            if not all(
                state["resources"].get(resource_type, 0) >= cost
                for resource_type, cost in costs.items()
            ):
                continue
            move_resources = new_resources.copy()
            for resource_type, cost in costs.items():
                move_resources[resource_type] -= cost

            move_robots = state["robots"].copy()
            move_robots.setdefault(robot_type, 0)
            move_robots[robot_type] += 1

            new_state = {
                "robots": move_robots,
                "resources": move_resources,
                "minute": state["minute"] + 1,
                "moves": state["moves"] + [{
                    "created_robot": robot_type,
                    "collected_resources": state["robots"],
                }]
            }
            heapq.heappush(queue, (sort_key(new_state), new_state))

        # We make no robots
        new_state = {
            "robots": state["robots"],
            "resources": new_resources,
            "minute": state["minute"] + 1,
            "moves": state["moves"] + [{
                "created_robot": None,
                "collected_resources": state["robots"],
            }]
        }

        heapq.heappush(queue, (sort_key(new_state), new_state))

    return best_state


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    blueprints = list(map(parse_blueprint, lines))

    print("RESULT", get_best_number_of_geodes(blueprints[1], 20))

    # minutes = 24
    # quality_levels = []

    # for blueprint in blueprints:
    #     best_state = get_best_number_of_geodes(blueprint, minutes)
    #     num_geodes = best_state["resources"].get("geode", 0)
    #     quality_level = blueprint.id * num_geodes
    #     print("BLUEPRINT", blueprint.id, num_geodes, quality_level)
    #     quality_levels.append(quality_level)

    # print("RESULT", sum(quality_levels))


if __name__ == '__main__':
    main()
