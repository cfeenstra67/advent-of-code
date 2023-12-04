import fileinput


def part_1_main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))

    numbers = []
    for line in lines:
        first_number = None
        last_number = None
        for char in line:
            if not char.isdigit():
                continue
            if first_number is None:
                first_number = char
            last_number = char
        
        if first_number is None or last_number is None:
            raise Exception(f"No numbers on line: {line}")

        numbers.append(int(first_number + last_number))
    
    print("SUM", sum(numbers))


number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part_2_main() -> None:
    lines = filter(None, map(str.strip, fileinput.input()))

    numbers = []
    for line in lines:
        first_number = None
        last_number = None
        idx = 0

        while idx < len(line):
            first_char = line[idx]
            if first_char.isdigit():
                number = first_char
                if first_number is None:
                    first_number = number
                last_number = number
            else:
                for word_idx, word in enumerate(number_words):
                    next_chars = line[idx: idx + len(word)]
                    if next_chars != word:
                        continue
                    number = str(word_idx + 1)

                    if first_number is None:
                        first_number = number
                    last_number = number

                    break
            
            idx += 1

        if first_number is None or last_number is None:
            raise Exception(f"No numbers on line: {line}")

        print("HERE", line, first_number, last_number, int(first_number + last_number))

        numbers.append(int(first_number + last_number))
    
    print("SUM", sum(numbers))


def main() -> None:
    part_2_main()


if __name__ == "__main__":
    main()
