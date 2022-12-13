import fileinput
from typing import Iterable, Dict, Any, List


class LineBuffer:
    """
    """
    def __init__(self, lines: Iterable[str]) -> None:

        def gen():
            for line in lines:
                while self.buffer:
                    yield self.buffer.pop(0)

                yield line

            while self.buffer:
                yield self.buffer.pop(0)

        self.gen = gen()
        self.buffer = []

    def push(self, line: str) -> None:
        self.buffer.append(line)

    def __iter__(self) -> Iterable[str]:
        return self.gen


def split_path(path: str) -> List[str]:
    if path == "/":
        return []
    return path[1:].split("/")


def process_cd(
    args: List[str],
    lines: LineBuffer,
    cwd: str,
    fs: Dict[str, Any]
) -> (str, Dict[str, Any]):
    loc = args[0]
    if loc == ".":
        return cwd, fs
    if loc == "..":
        components = cwd.split("/")
        return "/".join(components[:-1]), fs

    if loc[0] == "/":
        abs_path = loc
    else:
        abs_path = cwd + loc if cwd == "/" else "/".join([cwd, loc])

    components = split_path(abs_path)
    cwd_dict = fs
    for comp in components:
        cwd_dict = cwd_dict.setdefault(comp, {})

    return abs_path, fs


def process_ls(
    args: List[str],
    lines: LineBuffer,
    cwd: str,
    fs: Dict[str, Any]
) -> (str, Dict[str, Any]):
    ls_cwd = cwd
    if args:
        ls_cwd, fs = process_cd([args[0]], lines, cwd, fs)

    cwd_dict = fs
    for comp in split_path(ls_cwd):
        cwd_dict = cwd_dict[comp]

    for line in iterate_output_lines(lines):
        desc, name = line.strip().split()
        if desc == "dir":
            cwd_dict.setdefault(name, {})
            continue

        size = int(desc)
        cwd_dict[name] = size

    return cwd, fs


def process_command(
    command: str,
    lines: LineBuffer,
    cwd: str,
    fs: Dict[str, Any]
) -> (str, Dict[str, Any]):
    base, *args = command.split()
    if base == "cd":
        return process_cd(args, lines, cwd, fs)
    if base == "ls":
        return process_ls(args, lines, cwd, fs)
    raise RuntimeError(f"Invalid command: '{command}'")


def iterate_output_lines(lines: LineBuffer) -> Iterable[str]:
    for line in lines:
        if line.strip().startswith("$"):
            lines.push(line)
            return

        yield line


def process_lines(lines: Iterable[str]) -> (str, Dict[str, Any]):
    cwd = "/"
    fs = {}

    buffer = LineBuffer(lines)

    for line in buffer:
        if not line.strip():
            continue
        if line[0] == "$":
            command = line[1:].strip()
            cwd, fs = process_command(command, buffer, cwd, fs)
            continue
        raise RuntimeError(f"Unexpected line: '{line}'")

    return cwd, fs


def get_directories(fs):
    current_dir = "/"
    current_dir_size = 0
    for key, value in fs.items():
        if isinstance(value, dict):
            for subdir, size in get_directories(value):
                if subdir == "/":
                    current_dir_size += size
                yield current_dir + key + subdir, size
            continue

        current_dir_size += value

    yield current_dir, current_dir_size


def main():
    cwd, fs = process_lines(fileinput.input())
    total = 0
    max_size = 100_000
    used_size = 0
    for subdir, size in get_directories(fs):
        if subdir == "/":
            used_size = size
        if size > max_size:
            continue
        # print("DIR", subdir, size)
        total += size
    print("TOTAL", total)

    disk_size = 70000000
    update_size = 30000000

    unused_space = disk_size - used_size
    need_to_free = update_size - unused_space
    print("NEED TO FREE", need_to_free, need_to_free / disk_size)

    min_item = None, float("inf")
    for subdir, size in get_directories(fs):
        if size < need_to_free:
            continue
        if size < min_item[1]:
            min_item = subdir, size

    print("MIN", min_item)


if __name__ == '__main__':
    main()
