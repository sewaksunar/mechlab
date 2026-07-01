"""Entry point for `python -m mechlab`. Delegates straight to the CLI."""

from mechlab.interfaces.cli.commands import main

if __name__ == "__main__":
    main()
