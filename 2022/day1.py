import bisect
import fileinput

num_top_elves = 3

current_calories = 0
top_elves = []

for idx, line in enumerate(map(str.strip, fileinput.input())):
    if not line:
        bisect.insort(
            top_elves,
            (current_calories, idx),
        )
        if len(top_elves) > num_top_elves:
            top_elves.pop(0)
        current_calories = 0
        continue

    current_calories += int(line)

total = 0

for num, (calories, idx) in enumerate(top_elves):
    print(f"Elf #{num + 1} (index {idx}): {calories}")
    total += calories

print()
print("Total:", total)
