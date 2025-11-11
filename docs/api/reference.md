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
