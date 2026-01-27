import code
from rich.console import Console
from rich.panel import Panel

import mechlab as ml

console = Console()


def run_shell():
    console.print(
        Panel.fit(
            "[bold cyan]MechLab Interactive Shell[/bold cyan]\n"
            "Python-enabled • type exit() or Ctrl+D to quit",
            border_style="cyan",
        )
    )

    banner = (
        f"MechLab {ml.__version__}\n"
        "Preloaded:\n"
        "  import mechlab as ml\n"
    )

    local_vars = {
        "ml": ml,
    }

    code.interact(banner=banner, local=local_vars)
