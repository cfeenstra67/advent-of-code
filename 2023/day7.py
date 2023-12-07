import collections
import fileinput
from functools import cmp_to_key, partial
from typing import List


def card_to_num_part_1(card: str) -> int:
    if card.isdigit():
        return int(card)
    if card == "T":
        return 10
    if card == "J":
        return 11
    if card == "Q":
        return 12
    if card == "K":
        return 13
    if card == "A":
        return 14
    raise Exception(f"Invalid card: {card}")


def card_to_num_part_2(card: str) -> int:
    if card.isdigit():
        return int(card)
    if card == "T":
        return 10
    if card == "J":
        return 1
    if card == "Q":
        return 12
    if card == "K":
        return 13
    if card == "A":
        return 14
    raise Exception(f"Invalid card: {card}")


def get_best_type_part_1(hand: List[int]) -> int:
    counter = collections.Counter(hand)
    max_count = max(counter.values())
    min_count = min(counter.values())
    # Five of a kind
    if max_count == 5:
        return 0
    # Four of a kind
    if max_count == 4:
        return 1
    # Full house
    if max_count == 3 and min_count == 2:
        return 2
    # Three of a kind
    if max_count == 3:
        return 3
    # Two pair
    if sum(1 for v in counter.values() if v == 2) == 2:
        return 4
    # One pair
    if max_count == 2:
        return 5
    return 6


def get_best_type_part_2(hand: List[int]) -> int:
    jokers = 0
    others = []
    for card in hand:
        if card == 1:
            jokers += 1
        else:
            others.append(card)

    counter = collections.Counter(others)
    counts = sorted(counter.values())
    # Five of a kind
    if jokers >= 4 or counts[-1] + jokers == 5:
        return 0

    # Four of a kind
    if jokers >= 3 or counts[-1] + jokers == 4:
        return 1

    # Full house
    jokers_left_after_3 = jokers - (3 - counts[-1])
    if jokers_left_after_3 >= 1:
        return 2
    
    if jokers_left_after_3 == 0 and counts[-2] == 2:
        return 2

    # Three of a kind
    if jokers >= 2 or counts[-1] + jokers == 3:
        return 3

    # Two pair
    jokers_left_after_first_pair = jokers - (2 - counts[-1])
    if jokers_left_after_first_pair >= 1:
        return 4
    
    if counts[-2] == 2:
        return 4
    
    # One pair
    if jokers >= 1 or counts[-1] + jokers == 2:
        return 5

    return 6


def compare_hands(hand_1: List[int], hand_2: List[int], is_part_1: bool) -> int:
    if is_part_1:
        func = get_best_type_part_1
    else:
        func = get_best_type_part_2
    
    hand_1_score = func(hand_1)
    hand_2_score = func(hand_2)
    if hand_1_score < hand_2_score:
        return 1
    if hand_2_score < hand_1_score:
        return -1
    
    for hand_1_card, hand_2_card in zip(hand_1, hand_2):
        if hand_1_card > hand_2_card:
            return 1
        if hand_2_card > hand_1_card:
            return -1
    
    return 0


def main(is_part_1: bool) -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    hands = []

    if is_part_1:
        card_num_func = card_to_num_part_1
    else:
        card_num_func = card_to_num_part_2

    for line in lines:
        hand, bid = line.split()
        hand_nums = tuple(map(card_num_func, hand))
        bid_num = int(bid)
        hands.append((hand, hand_nums, bid_num))
    
    key_func = cmp_to_key(partial(compare_hands, is_part_1=is_part_1))
    sorted_hands = sorted(
        hands,
        key=lambda x: key_func(x[1]),
    )

    total_score = 0
    for idx, (_, _, bid) in enumerate(sorted_hands):
        total_score += bid * (idx + 1)
    
    print("TOTAL", total_score)


if __name__ == "__main__":
    main(is_part_1=False)
