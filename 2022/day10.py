import abc
import fileinput
from typing import List, Callable


class Device(abc.ABC):
    """
    """
    @abc.abstractmethod
    def run_cycle(self, cycle_no: int) -> None:
        raise NotImplementedError


class CPU(Device):
    
    def __init__(self) -> None:
        self.register = {"X": 1}
        self.operations = {
            "addx": op_addx,
            "noop": op_noop,
        }
        self.pending_instructions = []

    def handle_instruction(self, instruction: str) -> None:
        operation, *args = instruction.strip().split()
        if operation not in self.operations:
            raise ValueError(f"Invalid operation: {operation}")

        self.operations[operation](args, self)

    def run_cycle(self, cycle_no: int) -> None:
        if not self.pending_instructions:
            return
        cycles, func = self.pending_instructions[0]
        if cycles > 1:
            self.pending_instructions[0] = cycles - 1, func
            return
        self.pending_instructions.pop(0)
        func()

    def ready_for_instruction(self) -> bool:
        return not self.pending_instructions

    def add_task(self, cycles: int, func: Callable[[], None]) -> None:
        self.pending_instructions.append((cycles, func))

    def signal_strength(self, cycle_no: int) -> int:
        return cycle_no * self.register["X"]


def op_addx(args: List[str], cpu: CPU) -> None:
    
    def execute():
        cpu.register["X"] += int(args[0])

    cpu.add_task(2, execute)


def op_noop(args: List[str], cpu: CPU) -> None:
    cpu.add_task(1, lambda: None)


class CRT(Device):
    """
    """
    def __init__(
        self,
        cpu: CPU,
        width: int = 40,
        height: int = 6,
        sprite_width: int = 3,
    ) -> None:
        self.cpu = cpu
        self.width = width
        self.height = height
        self.sprite_width = sprite_width
        self.grid = [["." for _ in range(width)] for _ in range(height)]

    def run_cycle(self, cycle_no: int) -> None:
        x_offset = (cycle_no - 1) % (self.width * self.height)
        x_idx = x_offset % self.width
        y_idx = x_offset // self.width

        current_register = self.cpu.register["X"]
        sprite_radius = self.sprite_width // 2
        if x_idx - sprite_radius <= current_register <= x_idx + sprite_radius:
            self.grid[y_idx][x_idx] = "#"
        else:
            self.grid[y_idx][x_idx] = "."

    def print_grid(self) -> str:
        return "\n".join(map("".join, self.grid))


class Clock:
    """
    """
    def __init__(self, devices: List[Device]) -> None:
        self.devices = devices
        self.cycle_no = 1

    def run_cycle(self) -> None:
        for device in self.devices:
            device.run_cycle(self.cycle_no)
        self.cycle_no += 1


def main() -> None:
    cpu = CPU()
    crt = CRT(cpu)
    clock = Clock([crt, cpu])

    def is_relevant_cycle_no(number: int) -> bool:
        return number in range(20, 221, 40)

    total = 0

    for instruction in filter(None, map(str.strip, fileinput.input())):
        cpu.handle_instruction(instruction)
        while not cpu.ready_for_instruction():
            if is_relevant_cycle_no(clock.cycle_no):
                print("CYCLE", clock.cycle_no, cpu.signal_strength(clock.cycle_no))
                total += cpu.signal_strength(clock.cycle_no)
            clock.run_cycle()

    print("TOTAL", total)

    print("GRID")
    print(crt.print_grid())


if __name__ == '__main__':
    main()
