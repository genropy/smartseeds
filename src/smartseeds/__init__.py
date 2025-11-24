"""
SmartSeeds - Essential utilities that grow smart solutions.

A lightweight, zero-dependency library providing core utilities for the smart* ecosystem.
"""

__version__ = "0.3.1"

from .decorators import extract_kwargs
from .dict_utils import SmartOptions
from .typeutils import safe_is_instance
from .ascii_table import render_ascii_table, render_markdown_table

__all__ = [
    "extract_kwargs",
    "SmartOptions",
    "safe_is_instance",
    "render_ascii_table",
    "render_markdown_table",
]
