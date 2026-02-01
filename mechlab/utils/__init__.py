"""Utility helpers and environment detection.

Provides:
  - is_jupyter(): Check if running in Jupyter environment
"""

from .env import is_jupyter

__all__ = ["is_jupyter"]
