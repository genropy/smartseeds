"""
Dictionary utilities for SmartSeeds.

Provides utilities for dict manipulation and access patterns.
"""

from typing import Any, Dict, Optional


def dictExtract(
    source: Dict[str, Any],
    prefix: str,
    slice_prefix: bool = True,
    pop: bool = False,
) -> Dict[str, Any]:
    """
    Extract entries from a dictionary that match a given prefix.

    Args:
        source: Source dictionary to extract from
        prefix: Prefix to match keys against
        slice_prefix: If True, remove prefix from keys in result
        pop: If True, remove matching keys from source

    Returns:
        Dictionary with matching entries

    Example:
        >>> params = {'api_host': 'localhost', 'api_port': 8000, 'timeout': 30}
        >>> api_config = dictExtract(params, 'api_', slice_prefix=True, pop=True)
        >>> api_config
        {'host': 'localhost', 'port': 8000}
        >>> params
        {'timeout': 30}
    """
    result = {}

    keys_to_process = list(source.keys())
    for key in keys_to_process:
        if key.startswith(prefix):
            result_key = key[len(prefix):] if slice_prefix else key
            value = source.pop(key) if pop else source[key]
            result[result_key] = value

    return result


class Bag(dict):
    """
    A dictionary that supports attribute-style access.

    Attributes can be accessed via dot notation in addition to dict-style access.

    Example:
        >>> config = Bag(host='localhost', port=8000)
        >>> config.host
        'localhost'
        >>> config['port']
        8000
        >>> config.timeout = 30
        >>> config['timeout']
        30
    """

    def __getattr__(self, name: str) -> Any:
        """Get attribute via dot notation."""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Bag' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute via dot notation."""
        self[name] = value

    def __delattr__(self, name: str) -> None:
        """Delete attribute via dot notation."""
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'Bag' object has no attribute '{name}'")

    def __repr__(self) -> str:
        """String representation."""
        # Use dict.items() to avoid recursion since self.__dict__ is self
        items = ", ".join(f"{k}={v!r}" for k, v in dict.items(self))
        return f"Bag({items})"
