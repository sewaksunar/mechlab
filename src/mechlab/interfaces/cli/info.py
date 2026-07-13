"""
interfaces.cli.info — gathers install/version/dependency diagnostics.

Kept separate from commands.py (parsing/dispatch only) so the actual
"what do we know about this install" logic is independently testable
and reusable if a future GUI or web endpoint wants the same data.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import sys


def get_package_info() -> dict[str, str]:
    """Collect version, install location, and environment details.

    Returns:
        A dict of human-readable diagnostic fields. Never raises —
        any lookup failure is captured as an error string in the
        relevant field so `mechlab info` always succeeds and is safe
        to use as a first troubleshooting step.
    """
    info: dict[str, str] = {}

    # --- Version ---
    try:
        info["version"] = importlib.metadata.version("mechlab")
    except importlib.metadata.PackageNotFoundError:
        info["version"] = "NOT INSTALLED (running from source without install?)"

    # --- Install location ---
    spec = importlib.util.find_spec("mechlab")
    if spec is not None and spec.origin:
        info["location"] = spec.origin
    else:
        info["location"] = "unknown (mechlab not importable)"

    # --- Editable vs normal install ---
    info["install_type"] = _detect_install_type()

    # --- Python environment ---
    info["python_version"] = sys.version.split()[0]
    info["python_executable"] = sys.executable
    info["platform"] = platform.platform()

    # --- Optional dependency status ---
    info["matplotlib (plots extra)"] = _dependency_status("matplotlib")

    return info


def _detect_install_type() -> str:
    """Detect editable vs standard install by parsing direct_url.json.

    Uses actual JSON parsing rather than substring matching, since the
    file's whitespace/formatting isn't a stable contract to match against.
    """
    try:
        dist = importlib.metadata.distribution("mechlab")
    except importlib.metadata.PackageNotFoundError:
        return "unknown (package not found)"

    raw = dist.read_text("direct_url.json")
    if not raw:
        return "standard install"

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return "unknown (unparseable direct_url.json)"

    is_editable = data.get("dir_info", {}).get("editable", False)
    return "editable (uv sync / pip install -e)" if is_editable else "standard install"


def _dependency_status(module_name: str) -> str:
    """Report whether an optional dependency is installed, with its version."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return "not installed"
    try:
        version = importlib.metadata.version(module_name)
        return f"installed (v{version})"
    except importlib.metadata.PackageNotFoundError:
        return "installed (version unknown)"


def format_info_text(info: dict[str, str]) -> str:
    """Render package info as an aligned, human-readable block."""
    lines = ["=== mechlab package info ===", ""]
    width = max(len(key) for key in info)
    for key, value in info.items():
        lines.append(f"{key.ljust(width)} : {value}")
    return "\n".join(lines)
