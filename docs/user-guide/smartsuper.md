# smartsuper Guide

Complete guide to using the `smartsuper` decorator for automatic parent method calling.

## Overview

`smartsuper` is a decorator that automatically calls parent class methods before or after your method, eliminating repetitive `super()` calls.

**Key Features**:
- Method decorator with BEFORE/AFTER modes
- Universal class decorator (auto-decorates all overrides)
- Smart detection of class vs method decoration
- Magic methods excluded from auto-decoration for safety
- Zero boilerplate for inheritance chains

## Method Decorator - BEFORE

<!-- test: test_super.py::TestSmartSuperDecorator::test_smartsuper_calls_parent_before -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L10-L26)

The default `@smartsuper` calls the parent method **before** the current method:

```python
from smartseeds import smartsuper

class Base:
    def method(self):
        print("Base")

class Derived(Base):
    @smartsuper
    def method(self):
        print("Derived")

d = Derived()
d.method()
# Output:
# Base
# Derived
```

Perfect for initialization chains where parent setup must happen first.

## Method Decorator - AFTER

<!-- test: test_super.py::TestSmartSuperAfterDecorator::test_smartsuper_after_calls_parent_after -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L124-L140)

Use `@smartsuper.after` to call parent method **after** current method:

```python
class Base:
    def method(self):
        print("Base")

class Derived(Base):
    @smartsuper.after
    def method(self):
        print("Derived")

d = Derived()
d.method()
# Output:
# Derived
# Base
```

Perfect for cleanup operations where child cleanup happens before parent cleanup.

## Class Decorator - Auto-decoration

<!-- test: test_super.py::TestSmartSuperAllDecorator::test_smartsuper_all_decorates_all_overrides -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L278-L301)

Use `@smartsuper` on the **class** to auto-decorate all overridden methods:

```python
class Base:
    def foo(self):
        print("Base.foo")

    def bar(self):
        print("Base.bar")

@smartsuper  # Auto-decorates ALL overridden methods
class Derived(Base):
    def foo(self):
        print("Derived.foo")

    def bar(self):
        print("Derived.bar")

d = Derived()
d.foo()  # Base.foo → Derived.foo
d.bar()  # Base.bar → Derived.bar
```

**Note**: Magic methods (`__init__`, `__str__`, etc.) are **NOT** auto-decorated for safety.

## Mixing BEFORE and AFTER

<!-- test: test_super.py::TestSmartSuperAllDecorator::test_smartsuper_all_respects_explicit_after -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L303-L327)

You can mix BEFORE (default) and AFTER modes in the same class:

```python
class Base:
    def foo(self):
        print("Base.foo")

    def bar(self):
        print("Base.bar")

@smartsuper
class Derived(Base):
    def foo(self):
        print("Derived.foo")

    @smartsuper.after  # Explicit AFTER takes precedence
    def bar(self):
        print("Derived.bar")

d = Derived()
d.foo()  # Base.foo → Derived.foo (BEFORE)
d.bar()  # Derived.bar → Base.bar (AFTER)
```

## Arguments and Return Values

<!-- test: test_super.py::TestSmartSuperDecorator::test_smartsuper_with_arguments -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L45-L61)

Arguments are forwarded correctly to parent methods:

```python
class Base:
    def method(self, x, y=10):
        print(f"Base: x={x}, y={y}")

class Derived(Base):
    @smartsuper
    def method(self, x, y=10):
        print(f"Derived: x={x}, y={y}")

d = Derived()
d.method(5, y=20)
# Output:
# Base: x=5, y=20
# Derived: x=5, y=20
```

<!-- test: test_super.py::TestSmartSuperDecorator::test_smartsuper_with_return_value -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L80-L95)

The decorator returns the **decorated method's** return value:

```python
class Base:
    def method(self):
        return "Base"

class Derived(Base):
    @smartsuper
    def method(self):
        return "Derived"

d = Derived()
result = d.method()
print(result)  # "Derived"
```

## Multilevel Inheritance

<!-- test: test_super.py::TestSmartSuperDecorator::test_smartsuper_multilevel_inheritance -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L97-L118)

Works correctly with multiple inheritance levels:

```python
class Base:
    def method(self):
        print("Base")

class Middle(Base):
    @smartsuper
    def method(self):
        print("Middle")

class Derived(Middle):
    @smartsuper
    def method(self):
        print("Derived")

d = Derived()
d.method()
# Output:
# Base
# Middle
# Derived
```

Each level calls its immediate parent in the MRO (Method Resolution Order).

## Magic Methods

<!-- test: test_super.py::TestSmartSuperAllDecorator::test_smartsuper_all_skips_magic_methods -->

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_super.py#L329-L352)

Magic methods (`__dunder__`) are **excluded** from class auto-decoration:

```python
class Base:
    def __init__(self):
        print("Base.__init__")

    def normal_method(self):
        print("Base.normal")

@smartsuper
class Derived(Base):
    def __init__(self):
        print("Derived.__init__")  # NOT auto-decorated

    def normal_method(self):
        print("Derived.normal")  # Auto-decorated

d = Derived()
# Output: Derived.__init__ (only)

d.normal_method()
# Output:
# Base.normal
# Derived.normal
```

**Why?** Magic methods have special semantics and auto-calling parents can cause issues.

**Workaround**: Explicitly decorate magic methods if needed:

```python
class Derived(Base):
    @smartsuper
    def __init__(self):
        print("Derived.__init__")
```

## Use Cases

### Initialization Chains

```python
@smartsuper
class DatabaseService(BaseService):
    def setup(self):
        """Connect to database after base setup."""
        self.db = connect_to_database()
        print("Database connected")

    def teardown(self):
        """Disconnect before base teardown."""
        self.db.close()
        print("Database disconnected")
```

### Plugin Architecture

```python
class BasePlugin:
    def initialize(self):
        print("Base plugin initialization")

    def cleanup(self):
        print("Base plugin cleanup")

@smartsuper
class CachePlugin(BasePlugin):
    def initialize(self):
        """Initialize cache after base."""
        self.cache = {}
        print("Cache initialized")

    @smartsuper.after
    def cleanup(self):
        """Clear cache before base cleanup."""
        self.cache.clear()
        print("Cache cleared")
```

### Event Handlers

```python
class BaseHandler:
    def on_request(self, request):
        print("Logging request")
        self.log(request)

    def on_response(self, response):
        print("Logging response")
        self.log(response)

@smartsuper
class AuthHandler(BaseHandler):
    def on_request(self, request):
        """Check auth after logging."""
        if not self.verify_token(request.token):
            raise Unauthorized()

    def on_response(self, response):
        """Add auth headers after logging."""
        response.headers['X-Auth'] = 'verified'
```

### Mixins

```python
class LoggingMixin:
    def process(self, data):
        print(f"Processing: {data}")

class ValidationMixin:
    def process(self, data):
        print(f"Validating: {data}")
        if not data:
            raise ValueError("Empty data")

@smartsuper
class DataProcessor(LoggingMixin, ValidationMixin):
    def process(self, data):
        """Process after validation and logging."""
        result = self.transform(data)
        return result

processor = DataProcessor()
processor.process("test")
# Output:
# Validating: test
# Processing: test
# [actual processing]
```

## Comparison with Manual super()

**Without smartsuper** (manual):

```python
class Derived(Base):
    def method(self):
        super().method()  # Manual call
        print("Derived")
```

**With smartsuper** (automatic):

```python
class Derived(Base):
    @smartsuper
    def method(self):
        print("Derived")  # super() call automatic
```

**Benefits**:
- Less boilerplate
- Can't forget to call parent
- Consistent patterns across codebase
- Class decorator handles all methods at once

## When NOT to Use

Avoid `smartsuper` when:

1. **Conditional parent calls**: Parent should only be called sometimes
2. **Parent arguments differ**: Need to transform args before passing to parent
3. **Complex control flow**: Need logic between parent and child calls
4. **Return value matters**: Need to use or modify parent's return value

**Example where manual `super()` is better**:

```python
class Derived(Base):
    def method(self, x):
        # Need to transform argument before parent call
        if x > 0:
            result = super().method(x * 2)
            return result + 1
        else:
            # Don't call parent at all
            return 0
```

## Implementation Details

The `smartsuper` decorator uses:

- **`__new__`** to detect class vs method decoration
- **Descriptor protocol** (`__set_name__`, `__get__`) for method decoration
- **`__smartsuper_mode__`** attribute to track "before" or "after" mode
- **MRO inspection** to detect which methods override parent methods

**Universal decoration**: `@smartsuper` works on both classes and methods by detecting the target type in `__new__`.

## API Reference

```python
class smartsuper:
    """
    Decorator for calling superclass methods before or after the decorated method.

    Usage:
        @smartsuper              - On method: Call parent BEFORE
                                 - On class: Auto-decorate all overrides (BEFORE)
        @smartsuper.after        - On method: Call parent AFTER
        @smartsuper.all          - Explicit class decorator (same as @smartsuper on class)

    The decorator silently ignores if the superclass method doesn't exist.
    When used as class decorator, magic methods (__dunder__) are skipped for safety.
    """

    def __new__(cls, target):
        """Create decorator - detects if decorating a class or method."""
        ...

    def __init__(self, target: Any) -> None:
        """Initialize method decorator (only called for method decoration)."""
        ...

    @classmethod
    def after(cls, method: Callable) -> 'smartsuper':
        """Decorator variant that calls superclass method AFTER current method."""
        ...

    @classmethod
    def all(cls, target_class: type) -> type:
        """Apply smartsuper BEFORE to all methods that override a superclass method."""
        ...
```

## See Also

- [extract_kwargs Guide](extract-kwargs.md) - Prefix-based kwargs extraction
- [SmartOptions Guide](smart-options.md) - Intelligent option merging
- [Best Practices](best-practices.md) - Production patterns
- [API Reference](../api/reference.md) - Complete API documentation
