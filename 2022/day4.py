import fileinput


fully_contained = 0

overlapping = 0

for line in map(str.strip, fileinput.input()):
    if not line:
        continue
    range_str_1, range_str_2 = line.split(",")
    start_1, end_1 = map(int, range_str_1.split("-"))
    start_2, end_2 = map(int, range_str_2.split("-"))

    if start_1 <= start_2 and end_1 >= end_2:
        fully_contained += 1
    elif start_2 <= start_1 and end_2 >= end_1:
        fully_contained += 1

    if start_1 <= end_2 and end_1 >= start_2:
        overlapping += 1


print("FULLY CONTAINED", fully_contained)
print("OVERLAPPING", overlapping)
