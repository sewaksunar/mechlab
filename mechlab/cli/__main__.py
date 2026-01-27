import sys
from mechlab.cli.doctor import run_doctor
from mechlab.cli.shell import run_shell
from mechlab.cli.units import run_units

from mechlab.cli.math import run_math



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

    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: shell, doctor, units")
