import dataclasses as dc
import fileinput
import operator
from typing import List, Callable, Dict, Iterator, Tuple


OPS = {
    "*": operator.mul,
    "+": operator.add,
}


# def factors(num: int) -> Iterator[Tuple[int, int]]:
#     if num == 1:
#         return

#     lowest_factor = -1
#     for i in range(2, int(num ** .5) + 1):
#         if num % i == 0:
#             lowest_factor = i
#             break

#     if lowest_factor == -1:
#         yield num, 1
#         return

#     exponent = 1
#     while num % (lowest_factor ** (exponent + 1)) == 0:
#         exponent += 1

#     yield lowest_factor, exponent

#     rest = num // lowest_factor ** exponent
#     yield from factors(rest)


# class LargeNumber:
#     """
#     """
#     @classmethod
#     def from_int(cls, value: int) -> "LargeNumber":
#         return LargeNumber(dict(factors(value)))

#     def __init__(self, factors: Dict[int, int]) -> None:
#         self.factors = factors

#     def multiply(self, other: "LargeNumber") -> "LargeNumber":
#         factors = self.factors.copy()

#         for factor, exponent in other.factors.items():
#             if factor in self.factors:
#                 factors[factor] = self.factors[factor] + exponent
#             else:
#                 factors[factor] = exponent

#         return LargeNumber(factors)

#     def add(self, other: "LargeNumber") -> "LargeNumber":
#         common_factors = {}
#         self_remaining = {}
#         other_remaining = {}
#         for factor, exponent in other.factors.items():
#             if factor not in self.factors:
#                 other_remaining[factor] = exponent
#             else:
#                 common = min(self.factors[factor], exponent)
#                 common_factors[factor] = common
#                 self_remaining[factor] = self.factors[factor] - common
#                 other_remaining[factor] = exponent - common

#         for factor, exponent in self.factors.items():
#             if factor in other.factors:
#                 continue
#             self_remaining[factor] = exponent

#         print("HERE", common_factors, self_remaining, other_remaining)

#         if other_remaining or not other.factors:
#             self_value = 1
#             for factor, exponent in self_remaining.items():
#                 self_value *= factor ** exponent if exponent > 1 else factor

#             other_value = 1
#             for factor, exponent in other_remaining.items():
#                 other_value *= factor ** exponent if exponent > 1 else factor

#             value = self_value + other_value
#             new_factors = dict(factors(value))
#             print("VALUE", value, new_factors)
#             for factor, exponent in new_factors.items():
#                 if factor in common_factors:
#                     common_factors[factor] += exponent
#                 else:
#                     common_factors[factor] = exponent

#         elif self_remaining:
#             for factor, exponent in self_remaining.items():
#                 if factor in common_factors:
#                     common_factors[factor] += exponent
#                 else:
#                     common_factors[factor] = exponent

#         return LargeNumber(common_factors)

#     def __mul__(self, other: "LargeNumber") -> "LargeNumber":
#         if not isinstance(other, LargeNumber):
#             raise TypeError
#         return self.multiply(other)

#     def __add__(self, other: "LargeNumber") -> "LargeNumber":
#         if not isinstance(other, LargeNumber):
#             raise TypeError
#         return self.add(other)

#     def is_divisable_by(self, other: "LargeNumber") -> bool:
#         for factor, exponent in other.factors.items():
#             if factor not in self.factors:
#                 return False
#             if self.factors[factor] < exponent:
#                 return False
#         return True


@dc.dataclass
class Monkey:
    name: str
    # items: List[LargeNumber]
    items: List[int]
    operation: Callable[[int], int]
    divisible_by: int
    true_target: str
    false_target: str
    inspected_items: int = dc.field(init=False, default=0)

    def truncate_items(self, mod_value: int) -> None:
        self.items = [item % mod_value for item in self.items]

    def catch_item(self, worry_level: int) -> None:
        self.items.append(worry_level)

    def test(self, worry_level: int) -> str:
        return self.true_target if worry_level % self.divisible_by == 0 else self.false_target

    def take_turn(self, monkeys: Dict[str, "Monkey"]) -> None:
        for worry_level in self.items:
            # Monkey inspects item
            after_inspection = self.operation(worry_level)
            self.inspected_items += 1
            # # # Monkey gets bored, worry level divided by 3
            # after_inspection //= 3
            # Based on new worry level, monkey throws it to some other monkey
            new_monkey_id = self.test(after_inspection)
            # Other monkey catches item
            monkeys[new_monkey_id].catch_item(after_inspection)

        self.items.clear()


# class WorryTracker:

#     def __init__(self, monkeys: Dict[str, Monkey]) -> None:
#         self.monkeys = monkeys


def parse_operation(operation: str) -> Callable[[int], int]:
    _, _, name, op, other = operation.split()

    # name_func = lambda val: lambda x: x if val == "old" else LargeNumber.from_int(int(val))
    name_func = lambda val: lambda x: x if val == "old" else int(val)

    get_name = name_func(name)
    get_other = name_func(other)

    if op not in OPS:
        raise ValueError(f"Invalid operator: {op}")

    op_func = OPS[op]

    return lambda x: op_func(get_name(x), get_other(x))


def parse_test(test: str, if_true: str, if_false: str) -> Tuple[int, str, str]:
    true_target = if_true.split()[3]
    false_target = if_false.split()[3]

    # divisible_by = LargeNumber.from_int(int(test.split()[2]))
    # return lambda x: true_target if x.is_divisable_by(divisible_by) else false_target
    divisible_by = int(test.split()[2])
    return divisible_by, true_target, false_target


def parse_monkey(lines: Iterator[str]) -> Monkey:
    name_line = next(lines)
    name = name_line.split()[1].rstrip(":")

    start_line = next(lines)
    items_str = start_line.split(":", 1)[1]
    items = list(map(
        # lambda x: LargeNumber.from_int(int(x)),
        int,
        map(str.strip, items_str.split(",")))
    )

    op_line = next(lines)
    operation_str = op_line.split(":", 1)[1].strip()

    operation = parse_operation(operation_str)

    test_line = next(lines)
    test_str = test_line.split(":", 1)[1].strip()

    if_true_line = next(lines)
    if_true_str = if_true_line.split(":", 1)[1].strip()

    if_false_line = next(lines)
    if_false_str = if_false_line.split(":", 1)[1].strip()

    divisible_by, true_target, false_target = parse_test(test_str, if_true_str, if_false_str)

    return Monkey(
        name=name,
        items=items,
        operation=operation,
        divisible_by=divisible_by,
        true_target=true_target,
        false_target=false_target,
    )


def main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    monkeys = {}
    while True:
        try:
            monkey = parse_monkey(lines)
            monkeys[monkey.name] = monkey
        except StopIteration:
            break

    truncate_value = 1
    for monkey in monkeys.values():
        truncate_value *= monkey.divisible_by

    def print_monkeys():
        for name, monkey in monkeys.items():
            print("Monkey", monkey.name, ":", ", ".join(map(str, monkey.items)))

    for round_num in range(1, 10_001):
        for monkey in monkeys.values():
            monkey.truncate_items(truncate_value)
            monkey.take_turn(monkeys)

        print("Round", round_num)
        # print_monkeys()
        # print()
        for monkey in monkeys.values():
            print("Monkey", monkey.name, ":", monkey.inspected_items, "items")

    monkey_business = 1
    most_active = sorted(
        monkeys.values(),
        key=lambda x: -x.inspected_items
    )[:2]
    for monkey in most_active:
        monkey_business *= monkey.inspected_items

    print("Monkey business", monkey_business)


if __name__ == '__main__':
    main()
