import fileinput


def get_priority(letter):
    if letter >= 'a':
        return 1 + ord(letter) - ord('a')
    return 27 + ord(letter) - ord('A')


# total_priority = 0

# for line in map(str.strip, fileinput.input()):
#     compartment_1 = line[:len(line) // 2]
#     compartment_2 = line[len(line) // 2:]
#     common_item = (set(compartment_1) & set(compartment_2)).pop()
#     total_priority += get_priority(common_item)

# print("TOTAL", total_priority)


def chunks(iterable, n):
    i = iter(iterable)
    chunk = list(map(next, [i] * n))
    yield chunk
    while True:
        try:
            item = next(i)
        except StopIteration:
            break
        else:
            yield (item,) + tuple(map(next, [i] * (n - 1)))


total_priority = 0

for chunk in chunks(map(str.strip, fileinput.input()), 3):
    common_item = set.intersection(*map(set, chunk)).pop()
    total_priority += get_priority(common_item)

print("TOTAL", total_priority)
