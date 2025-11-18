"""
SmartSeeds - Essential utilities that grow smart solutions.

A lightweight, zero-dependency library providing core utilities for the smart* ecosystem.
"""

__version__ = "0.2.1"

from .decorators import extract_kwargs, smartsuper
from .dict_utils import SmartOptions

__all__ = [
    "extract_kwargs",
    "SmartOptions",
    "smartsuper",
]
