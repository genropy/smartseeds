"""
Decorators for SmartSeeds.

Provides utilities for extracting and grouping keyword arguments.
"""

from functools import wraps
from typing import Callable, Any


def extract_kwargs(**extract_specs: Any) -> Callable:
    """
    Decorator to extract and group keyword arguments by prefix.

    This decorator allows methods to accept kwargs with prefixes (e.g., `logging_level`,
    `cache_ttl`) and automatically groups them into separate kwargs dictionaries
    (e.g., `logging_kwargs`, `cache_kwargs`).

    Args:
        **extract_specs: Specifications for kwargs extraction. Each key is a prefix name,
                        and the value can be:
                        - True: Extract and pop kwargs with this prefix
                        - dict: Extract with custom options (slice_prefix, pop, etc.)

    Example:
        >>> @extract_kwargs(logging=True, cache=True)
        ... def setup(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
        ...     print(f"Logging: {logging_kwargs}")
        ...     print(f"Cache: {cache_kwargs}")
        ...
        >>> setup(name="api", logging_level="INFO", cache_ttl=300, timeout=30)
        # logging_kwargs={'level': 'INFO'}
        # cache_kwargs={'ttl': 300}
        # kwargs={'timeout': 30}

    Dict style also supported:
        >>> setup(name="api", logging={'level': 'INFO'}, cache={'ttl': 300})
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Process each extract spec
            for extract_key, extract_value in extract_specs.items():
                grp_key = f'{extract_key}_kwargs'

                # Start with explicitly provided kwargs dict
                current = kwargs.pop(grp_key, None) or {}

                # Check if prefix is provided as dict (e.g., logging={'level': 'INFO'})
                activated = False
                if extract_key in kwargs:
                    prefix_value = kwargs.pop(extract_key)
                    if isinstance(prefix_value, dict):
                        current.update(prefix_value)
                        activated = True
                    elif prefix_value is True:
                        activated = True  # Just activate with defaults

                # Extract prefixed kwargs (e.g., logging_level → level)
                prefix = f'{extract_key}_'
                keys_to_process = list(kwargs.keys())
                for key in keys_to_process:
                    if key.startswith(prefix):
                        param_name = key[len(prefix):]  # Remove prefix
                        current[param_name] = kwargs.pop(key)
                        activated = True

                # Add extracted kwargs back (None if not activated, {} if activated but empty)
                kwargs[grp_key] = current if (current or activated) else None

            return func(*args, **kwargs)

        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator
