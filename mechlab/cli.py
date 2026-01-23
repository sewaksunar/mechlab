import argparse
import sys
import platform
from mechlab import __version__

def main():
    parser = argparse.ArgumentParser(description="MechLab CLI")
    parser.add_argument("-v", "--version", action="version", version=f"MechLab {__version__}")
    
    subparsers = parser.add_subparsers(dest="command")

    # Command: info (Author & Project details)
    info_parser = subparsers.add_parser("info", help="Show author and project metadata")

    # Command: check (System & Dependency check)
    check_parser = subparsers.add_parser("check", help="Check system compatibility")

    args = parser.parse_args()

    if args.command == "info":
        print("--- MechLab Project Info ---")
        print(f"Version:  {__version__}")
        print("Author:   Sewak Sunar")
        print("Email:    sewaksunar@hotmail.com")
        print("GitHub:   https://github.com/sewaksunar/mechlab")
        print("License:  MIT")

    elif args.command == "check":
        print("--- System Compatibility Check ---")
        print(f"Python:   {platform.python_version()}")
        print(f"OS:       {platform.system()} {platform.release()}")
        # Check if important dependencies are found
        try:
            import numpy
            print(f"NumPy:    Found ({numpy.__version__})")
        except ImportError:
            print("NumPy:    NOT FOUND")
        
    elif args.command is None:
        parser.print_help()

if __name__ == "__main__":
    main()