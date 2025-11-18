# API Reference

Complete API documentation for SmartSeeds.

## extract_kwargs

```{eval-rst}
.. autofunction:: smartseeds.extract_kwargs
```

### Function Signature

```python
def extract_kwargs(
    _adapter: Optional[str] = None,
    _dictkwargs: Optional[Dict[str, Any]] = None,
    **extraction_specs: Any
) -> Callable[[F], F]
```

### Parameters

**_adapter** : `Optional[str]`
: Name of a method on `self` that will be called to pre-process `kwargs` before extraction.
  The adapter method receives the `kwargs` dict and can modify it in-place.

**_dictkwargs** : `Optional[Dict[str, Any]]`
: Optional dictionary of extraction specifications. When provided, this is used instead of `**extraction_specs`.
  Useful for dynamic extraction specifications.

**extraction_specs** : `Any`
: Keyword arguments where keys are prefix names and values specify extraction behavior:
  - `True`: Extract parameters with this prefix and remove them from source (`pop=True`)
  - `dict`: Custom extraction options (`pop`, `slice_prefix`, `is_list`)

### Returns

**Callable[[F], F]**
: Decorated function that performs kwargs extraction

### Examples

See [extract_kwargs Guide](../user-guide/extract-kwargs.md) for detailed examples.

## smartsuper

```{eval-rst}
.. autoclass:: smartseeds.smartsuper
   :members:
   :special-members: __new__, __init__, __get__, __set_name__
```

### Class Signature

```python
class smartsuper:
    """Decorator for calling superclass methods before or after the decorated method."""

    def __new__(cls, target) -> Union['smartsuper', type]:
        """Create decorator - detects if decorating a class or method."""

    def __init__(self, target: Any) -> None:
        """Initialize method decorator (only called for method decoration)."""

    @classmethod
    def after(cls, method: Callable) -> 'smartsuper':
        """Decorator variant that calls superclass method AFTER current method."""

    @classmethod
    def all(cls, target_class: type) -> type:
        """Apply smartsuper BEFORE to all methods that override a superclass method."""
```

### Usage Modes

**Method Decorator (BEFORE)**:
```python
class Derived(Base):
    @smartsuper
    def method(self):
        pass  # Base.method() called BEFORE this
```

**Method Decorator (AFTER)**:
```python
class Derived(Base):
    @smartsuper.after
    def method(self):
        pass  # Base.method() called AFTER this
```

**Class Decorator**:
```python
@smartsuper
class Derived(Base):
    def method(self):
        pass  # Auto-decorated, Base.method() called BEFORE
```

### Behavior

- **BEFORE mode** (default): Calls parent method, then current method
- **AFTER mode**: Calls current method, then parent method
- **Class mode**: Auto-decorates all overridden methods (BEFORE), skips magic methods
- **Silent**: Doesn't fail if parent method doesn't exist
- **Return value**: Returns the decorated method's return value (not parent's)

### Notes

- Magic methods (`__dunder__`) are NOT auto-decorated when using class mode
- Explicit decoration of magic methods is still possible
- Uses descriptor protocol for proper method binding
- `__smartsuper_mode__` attribute tracks "before" or "after" mode

### Examples

See [smartsuper Guide](../user-guide/smartsuper.md) for detailed examples.

## SmartOptions

```{eval-rst}
.. autoclass:: smartseeds.SmartOptions
   :members:
   :special-members: __init__
```

### Class Signature

```python
class SmartOptions(SimpleNamespace):
    def __init__(
        self,
        incoming: Optional[Mapping[str, Any]] = None,
        defaults: Optional[Mapping[str, Any]] = None,
        *,
        ignore_none: bool = False,
        ignore_empty: bool = False,
        filter_fn: Optional[Callable[[str, Any], bool]] = None,
    )
```

### Parameters

**incoming** : `Optional[Mapping[str, Any]]`
: Mapping with runtime kwargs. Values override defaults after filtering. Can be None.

**defaults** : `Optional[Mapping[str, Any]]`
: Mapping with baseline options. Can be None.

**ignore_none** : `bool`
: When True, skip incoming entries where the value is `None`. Default: False.

**ignore_empty** : `bool`
: When True, skip empty strings/collections from incoming entries. Default: False.
  Empty values include: `""`, `[]`, `()`, `{}`, `set()`, etc.

**filter_fn** : `Optional[Callable[[str, Any], bool]]`
: Optional custom filter function receiving `(key, value)` and returning True if the pair should be kept.
  Applied before `ignore_none` and `ignore_empty`.

### Methods

**as_dict() → Dict[str, Any]**
: Return a copy of current options as a dictionary.

### Examples

See [SmartOptions Guide](../user-guide/smart-options.md) for detailed examples.

## Helper Functions

### filtered_dict

```python
def filtered_dict(
    data: Optional[Mapping[str, Any]],
    filter_fn: Optional[Callable[[str, Any], bool]] = None,
) -> Dict[str, Any]
```

Return a dict filtered through `filter_fn`.

**Parameters**:
- `data`: Source mapping (can be None)
- `filter_fn`: Optional filter callable `(key, value) → bool`

**Returns**: Filtered dictionary

### make_opts

```python
def make_opts(
    incoming: Optional[Mapping[str, Any]],
    defaults: Optional[Mapping[str, Any]] = None,
    *,
    filter_fn: Optional[Callable[[str, Any], bool]] = None,
    ignore_none: bool = False,
    ignore_empty: bool = False,
) -> SimpleNamespace
```

Merge incoming kwargs with defaults and return a SimpleNamespace.

Similar to `SmartOptions` but returns a plain `SimpleNamespace` without the `as_dict()` method.

## dictExtract (Internal)

Internal utility function used by `extract_kwargs`. Not part of the public API.

```python
def dictExtract(
    mydict: dict,
    prefix: str,
    pop: bool = False,
    slice_prefix: bool = True,
    is_list: bool = False
) -> dict
```

Returns a dict of items with keys starting with prefix.

---

## Type Definitions

```python
F = TypeVar('F', bound=Callable[..., Any])
```

Type variable for decorated function preservation.

---

## See Also

- [User Guide](../user-guide/extract-kwargs.md) - Complete feature documentation
- [Examples](../examples/index.md) - Real-world usage examples
- [Best Practices](../user-guide/best-practices.md) - Production patterns
