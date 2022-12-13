import sys


def get_eof_bytes(file, chunk_size=1024):
    processed = 0
    # eof_length = 4
    eof_length = 14

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break

        buffer = []
        for idx, char in enumerate(chunk):
            buffer.append(char)
            if len(buffer) > eof_length:
                buffer.pop(0)

            processed += 1

            if len(set(buffer)) == eof_length:
                return processed

    raise ValueError("EOF not found")


def main():
    print(get_eof_bytes(sys.stdin))


if __name__ == '__main__':
    main()
