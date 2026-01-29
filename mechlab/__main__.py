import argparse
from mechlab.cli.stress import run_stress
from mechlab.cli.beam import run_beam

def main():
    parser = argparse.ArgumentParser(prog="mechlab")
    subparsers = parser.add_subparsers(dest="module")

    stress_parser = subparsers.add_parser("stress")
    stress_parser.add_argument("rest", nargs=argparse.REMAINDER)

    beam_parser = subparsers.add_parser("beam")
    beam_parser.add_argument("rest", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.module == "stress":
        run_stress(args.rest)
    elif args.module == "beam":
        run_beam(args.rest)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
