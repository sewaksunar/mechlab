import sys

from mechlab.cli.doctor import run_doctor
from mechlab.cli.shell import run_shell
from mechlab.cli.units import run_units
from mechlab.cli.math import run_math
from mechlab.cli.stress import run_stress   # 👈 NEW
from mechlab.cli.beam import run_beam



def main():
    args = sys.argv[1:]

    if not args:
        run_shell()
        return

    cmd, *rest = args

    if cmd == "doctor":
        run_doctor(
            verbose="--verbose" in rest,
            json_mode="--json" in rest,
        )

    elif cmd == "shell":
        run_shell()

    elif cmd == "units":
        run_units(rest)

    elif cmd == "math":
        run_math(rest)

    elif cmd == "stress":               # 👈 NEW
        run_stress(rest)
    
    elif cmd == "beam":
        run_beam(rest)

    else:
        print(f"Unknown command: {cmd}")
        print("Available commands:")
        print("  shell, doctor, units, math, stress")


if __name__ == "__main__":
    main()
