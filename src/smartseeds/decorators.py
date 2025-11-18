"""
Decorators for SmartSeeds.

Provides utilities for extracting and grouping keyword arguments.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from .dict_utils import dictExtract

F = TypeVar("F", bound=Callable[..., Any])

# Constants to avoid recreating dicts
_DEFAULT_EXTRACT_OPTIONS = {"slice_prefix": True, "pop": False, "is_list": False}
_POP_EXTRACT_OPTIONS = {"slice_prefix": True, "pop": True, "is_list": False}


def extract_kwargs(
    _adapter: str | None = None, _dictkwargs: dict[str, Any] | None = None, **extraction_specs: Any
) -> Callable[[F], F]:
    """A decorator that extracts ``**kwargs`` into sub-families by prefix.

    This decorator allows methods to accept kwargs with prefixes (e.g., `logging_level`,
    `cache_ttl`) and automatically groups them into separate kwargs dictionaries
    (e.g., `logging_kwargs`, `cache_kwargs`).

    Args:
        _adapter: Optional name of a method on self that will pre-process kwargs.
                 The adapter method receives kwargs dict and can modify it in-place.
        _dictkwargs: Optional dict to use instead of ``**extraction_specs``.
                    Useful for dynamic extraction specifications.
        **extraction_specs: Extraction specifications where keys are prefix names.
                          Values can be:
                          - True: Extract and remove (pop=True)
                          - dict: Custom options (slice_prefix, pop, is_list)

    Returns:
        Decorated function that extracts kwargs by prefix.

    Example:
        >>> @extract_kwargs(palette=True, dialog=True, default=True)
        ... def my_method(self, pane, table=None,
        ...              palette_kwargs=None, dialog_kwargs=None, default_kwargs=None,
        ...              **kwargs):
        ...     pass
        ...
        >>> # Call with prefixed parameters
        >>> obj.my_method(palette_height='200px', palette_width='300px',
        ...              dialog_height='250px')
        >>> # palette_kwargs={'height': '200px', 'width': '300px'}
        >>> # dialog_kwargs={'height': '250px'}

    Notes:
        - The decorated function MUST have `{prefix}_kwargs` parameters for each prefix
        - Reserved keyword 'class' is automatically renamed to '_class'
        - Works with both class methods (with self) and standalone functions
        - Maintains 100% compatibility with original Genropy implementation
    """
    # Use _dictkwargs if provided, otherwise use extraction_specs
    # Note: We use a different variable name to avoid shadowing the parameter
    specs_to_use = _dictkwargs if _dictkwargs is not None else extraction_specs

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if this is a method (has self) or function
            # For methods: self is args[0]
            # For functions: no self
            has_self = len(args) > 0 and hasattr(args[0].__class__, func.__name__)
            self_arg = args[0] if has_self else None

            # Call adapter if specified and this is a method
            if _adapter and self_arg is not None:
                adapter_method = getattr(self_arg, _adapter, None)
                if adapter_method is not None:
                    adapter_method(kwargs)

            # Process each extraction specification
            for extract_key, extract_value in specs_to_use.items():
                grp_key = f"{extract_key}_kwargs"

                # Get existing grouped kwargs (if explicitly passed)
                current = kwargs.pop(grp_key, None)
                if current is None:
                    current = {}
                elif not isinstance(current, dict):
                    # Edge case: someone passed non-dict, convert to dict
                    current = {}

                # Determine extraction options based on extract_value
                if extract_value is True:
                    # True means: extract and remove from source
                    extract_options = _POP_EXTRACT_OPTIONS
                elif isinstance(extract_value, dict):
                    # Dict means: custom options
                    extract_options = {**_DEFAULT_EXTRACT_OPTIONS, **extract_value}
                else:
                    # Default: extract but don't remove from source
                    extract_options = _DEFAULT_EXTRACT_OPTIONS

                # Extract prefixed kwargs
                prefix = f"{extract_key}_"
                extracted = dictExtract(kwargs, prefix, **extract_options)

                # Merge extracted kwargs with current
                current.update(extracted)

                # Set the grouped kwargs back
                # Always set as dict (never None), matching original behavior
                kwargs[grp_key] = current

            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


class smartsuper:
    """Decorator for calling superclass methods before or after the decorated method.

    Usage:
        @smartsuper
            On method: Call superclass method BEFORE current method
            On class: Auto-decorate all overridden methods (skips magic methods)
        @smartsuper.after
            Call superclass method AFTER current method
        @smartsuper.all
            Explicit class decorator (equivalent to @smartsuper on class)

    The decorator silently ignores if the superclass method doesn't exist.
    When used as class decorator, magic methods (__dunder__) are skipped for safety.

    Example (method decorator):
        >>> class Base:
        ...     def setup(self):
        ...         print("Base setup")
        ...
        >>> class Derived(Base):
        ...     @smartsuper
        ...     def setup(self):
        ...         print("Derived setup")
        ...
        >>> d = Derived()
        >>> d.setup()
        Base setup
        Derived setup

    Example (class decorator):
        >>> class Base:
        ...     def foo(self): pass
        ...     def bar(self): pass
        ...
        >>> @smartsuper
        ... class Derived(Base):
        ...     def foo(self): pass  # Will call Base.foo() before
        ...     def bar(self): pass  # Will call Base.bar() before
    """

    def __new__(cls, target):
        """Create decorator - detects if decorating a class or method."""
        # If decorating a class, apply class decoration
        if isinstance(target, type):
            return cls._decorate_class(target)

        # Otherwise, create method decorator instance
        instance = super().__new__(cls)
        return instance

    def __init__(self, target: Any) -> None:
        """Initialize method decorator (only called for method decoration)."""
        # Skip if this was a class decoration (target is already processed)
        if isinstance(target, type):
            return

        self.method = target
        self.after_call = False
        self.owner: type | None = None
        self.name: str | None = None
        target.__smartsuper_mode__ = "before"

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Callable[..., Any]:
        if obj is None:
            return self

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            parent_method = getattr(super(self.owner, obj), self.name, None)

            if not self.after_call:
                if parent_method:
                    parent_method(*args, **kwargs)
                return self.method(obj, *args, **kwargs)
            else:
                result = self.method(obj, *args, **kwargs)
                if parent_method:
                    parent_method(*args, **kwargs)
                return result

        return wrapper

    @classmethod
    def after(cls, method: Callable[..., Any]) -> "smartsuper":
        """Decorator variant that calls superclass method AFTER current method."""
        instance = object.__new__(cls)
        instance.method = method
        instance.after_call = True
        instance.owner = None
        instance.name = None
        method.__smartsuper_mode__ = "after"
        return instance

    @classmethod
    def all(cls, target_class: type) -> type:
        """Apply smartsuper BEFORE to all methods that override a superclass method.

        Methods explicitly decorated with @smartsuper.after are left unchanged.
        Magic methods (__dunder__) are automatically skipped for safety.

        Example:
            >>> class Base:
            ...     def foo(self): pass
            ...     def bar(self): pass
            ...
            >>> @smartsuper.all
            ... class Derived(Base):
            ...     def foo(self): pass  # Will call Base.foo() before
            ...     def bar(self): pass  # Will call Base.bar() before
        """
        return cls._decorate_class(target_class)

    @classmethod
    def _decorate_class(cls, target_class: type) -> type:
        """Internal method to decorate all overridden methods in a class."""
        for name, attr in list(target_class.__dict__.items()):
            # Skip magic methods
            if name.startswith("__") and name.endswith("__"):
                continue

            # Skip non-callable
            if not callable(attr):
                continue

            # Skip methods already decorated with smartsuper.after
            if getattr(attr, "__smartsuper_mode__", None) == "after":
                continue

            # Check if this method overrides a superclass method
            for base in target_class.__mro__[1:]:
                if hasattr(base, name):
                    # Don't decorate twice if already manually decorated
                    if getattr(attr, "__smartsuper_mode__", None) == "before":
                        break

                    # Automatically decorate as BEFORE
                    decorated = object.__new__(cls)
                    decorated.method = attr
                    decorated.after_call = False
                    decorated.owner = None
                    decorated.name = None
                    attr.__smartsuper_mode__ = "before"
                    decorated.__set_name__(target_class, name)
                    setattr(target_class, name, decorated)
                    break

        return target_class
