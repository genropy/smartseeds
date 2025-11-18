<div align="center">
  <img src="docs/assets/logo.png" alt="SmartSeeds Logo" width="200"/>
</div>

# SmartSeeds 🌱

**Essential utilities that grow smart solutions**

SmartSeeds is a lightweight, zero-dependency Python library providing core utilities for the smart* ecosystem (smartroute, smartasync, etc.). Think of it as the seeds from which smart solutions grow.

[![PyPI version](https://img.shields.io/pypi/v/smartseeds.svg)](https://pypi.org/project/smartseeds/)
[![Tests](https://github.com/genropy/smartseeds/actions/workflows/test.yml/badge.svg)](https://github.com/genropy/smartseeds/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/genropy/smartseeds/branch/main/graph/badge.svg)](https://codecov.io/gh/genropy/smartseeds)
[![Documentation](https://readthedocs.org/projects/smartseeds/badge/?version=latest)](https://smartseeds.readthedocs.io/en/latest/)
[![LLM Docs](https://img.shields.io/badge/LLM-docs-blue)](LLM.md)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- **`extract_kwargs`**: Decorator for extracting and grouping keyword arguments by prefix
- **`smartsuper`**: Decorator for automatic superclass method calls (before/after)
- **`SmartOptions`**: Intelligent options merging with filtering and defaults
- **Three flexible styles**: Prefix style, dict style, and boolean activation
- **Zero dependencies**: Pure Python standard library
- **Full type hints**: Complete typing support

## Installation

```bash
pip install smartseeds
```

## Quick Start

### extract_kwargs Decorator

Extract kwargs by prefix into separate parameter groups - supports three convenient styles:

```python
from smartseeds import extract_kwargs

@extract_kwargs(logging=True, cache=True)
def setup_service(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
    print(f"Logging config: {logging_kwargs}")
    print(f"Cache config: {cache_kwargs}")
    print(f"Other: {kwargs}")

# Style 1: Prefix style (most explicit)
setup_service(
    name="api",
    logging_level="INFO",      # → logging_kwargs={'level': 'INFO'}
    logging_format="json",     # → logging_kwargs={'format': 'json'}
    cache_ttl=300,             # → cache_kwargs={'ttl': 300}
    timeout=30                 # → kwargs={'timeout': 30}
)

# Style 2: Dict style (compact)
setup_service(
    name="api",
    logging={'level': 'INFO', 'format': 'json'},
    cache={'ttl': 300}
)

# Style 3: Boolean activation (use defaults)
setup_service(
    name="api",
    logging=True,  # → logging_kwargs={} (empty dict for defaults)
    cache=True
)
```

### smartsuper Decorator

Automatically call parent class methods before or after your method - perfect for initialization chains and cleanup:

```python
from smartseeds import smartsuper

# Style 1: Method decorator (BEFORE)
class Base:
    def setup(self):
        print("Base setup")

class Derived(Base):
    @smartsuper  # Calls Base.setup() BEFORE Derived.setup()
    def setup(self):
        print("Derived setup")

d = Derived()
d.setup()
# Output:
# Base setup
# Derived setup

# Style 2: Method decorator (AFTER)
class Base:
    def cleanup(self):
        print("Base cleanup")

class Derived(Base):
    @smartsuper.after  # Calls Base.cleanup() AFTER Derived.cleanup()
    def cleanup(self):
        print("Derived cleanup")

d = Derived()
d.cleanup()
# Output:
# Derived cleanup
# Base cleanup

# Style 3: Class decorator (auto-decorate all overrides)
class Base:
    def foo(self):
        print("Base.foo")
    def bar(self):
        print("Base.bar")

@smartsuper  # Auto-decorates ALL overridden methods (BEFORE by default)
class Derived(Base):
    def foo(self):
        print("Derived.foo")

    @smartsuper.after  # Explicit AFTER takes precedence
    def bar(self):
        print("Derived.bar")

d = Derived()
d.foo()  # Base.foo → Derived.foo
d.bar()  # Derived.bar → Base.bar

# Note: Magic methods (__init__, __str__, etc.) are NOT auto-decorated
# You can still explicitly decorate them if needed
```

### SmartOptions - Intelligent Option Merging

Merge incoming options with defaults, with automatic filtering:

```python
from smartseeds import SmartOptions

# Basic merge: incoming overrides defaults
opts = SmartOptions(
    incoming={'timeout': 10, 'retries': None},
    defaults={'timeout': 5, 'retries': 3, 'debug': False}
)
print(opts.timeout)  # 10 (from incoming)
print(opts.retries)  # None (from incoming)
print(opts.debug)    # False (from defaults)

# Ignore None values
opts = SmartOptions(
    incoming={'timeout': None, 'retries': 5},
    defaults={'timeout': 30, 'retries': 3},
    ignore_none=True  # Skip None from incoming
)
print(opts.timeout)  # 30 (default kept, None ignored)
print(opts.retries)  # 5 (from incoming)

# Ignore empty collections
opts = SmartOptions(
    incoming={'tags': [], 'name': ''},
    defaults={'tags': ['prod'], 'name': 'default'},
    ignore_empty=True  # Skip empty strings/lists/dicts
)
print(opts.tags)  # ['prod'] (default kept)
print(opts.name)  # 'default' (default kept)

# Convert back to dict
config_dict = opts.as_dict()
```

### Use in smart* Ecosystem

SmartSeeds is designed to be used by other smart* tools:

```python
# In smartroute, smartasync, etc.
from smartseeds import extract_kwargs

class Service:
    @extract_kwargs(logging=True, async_mode=True)
    def __init__(self, name=None, logging_kwargs=None, async_kwargs=None, **kwargs):
        # Plugin configuration extracted automatically
        if logging_kwargs:
            self.plug('logging', **logging_kwargs)
        if async_kwargs:
            self.plug('async', **async_kwargs)
```

## Why extract_kwargs?

Traditional approaches to nested configuration have problems:

**❌ Explicit parameters (verbose)**
```python
def connect(host, port, logging_level=None, logging_format=None, logging_file=None):
    logger = Logger(level=logging_level, format=logging_format, file=logging_file)
```

**❌ Catch-all kwargs (unclear)**
```python
def connect(host, port, **kwargs):
    # What kwargs are valid? Users don't know!
    logger = Logger(**kwargs)
```

**✅ extract_kwargs (clear + flexible)**
```python
@extract_kwargs(logging=True)
def connect(host, port, logging_kwargs=None):
    if logging_kwargs:
        logger = Logger(**logging_kwargs)

# All these work and are clear:
connect('localhost', 8000, logging_level='INFO')
connect('localhost', 8000, logging={'level': 'INFO'})
connect('localhost', 8000, logging=True)
```

## Documentation

Full documentation available at: https://smartseeds.readthedocs.io

## Part of the Smart* Family

SmartSeeds is part of the Genropy smart* toolkit:

- [smartroute](https://github.com/genropy/smartroute) - Instance-scoped routing engine with plugin architecture
- [smartasync](https://github.com/genropy/smartasync) - Async utilities
- [smartpublisher](https://github.com/genropy/smartpublisher) - CLI/API framework based on SmartRoute

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.
