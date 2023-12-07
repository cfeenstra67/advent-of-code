import fileinput


def number_of_ways_to_beat_best_time(time: int, max_distance: int) -> int:
    min_hold_time = None
    max_hold_time = None

    for hold_seconds in range(time + 1):
        distance = hold_seconds * (time - hold_seconds)
        if distance > max_distance:
            min_hold_time = hold_seconds
            break
    
    assert min_hold_time is not None

    for hold_seconds in range(time, -1, -1):
        distance = hold_seconds * (time - hold_seconds)
        if distance > max_distance:
            max_hold_time = hold_seconds
            break
    
    assert max_hold_time is not None

    return max_hold_time - min_hold_time + 1


def main(is_part_1: bool) -> None:
    lines = filter(None, map(str.strip, fileinput.input()))
    times = []
    distances = []
    for line in lines:
        word, *number_strs = line.split()
        if is_part_1:
            numbers = list(map(int, number_strs))
        else:
            numbers = [int("".join(number_strs))]
        if word == "Time:":
            times = numbers
        else:
            distances = numbers

    assert len(times) == len(distances)

    races = list(zip(times, distances))

    product = 1
    for time, distance in races:
        product *= number_of_ways_to_beat_best_time(time, distance)

    print("RESULT", product)


if __name__ == "__main__":
    main(is_part_1=False)
