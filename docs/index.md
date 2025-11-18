<div align="center">
  <img src="_static/logo.png" alt="SmartSeeds Logo" width="200"/>
</div>

# SmartSeeds 🌱

**Essential utilities that grow smart solutions**

SmartSeeds is a lightweight, zero-dependency Python library providing core utilities for the smart* ecosystem (smartroute, smartasync, etc.). Think of it as the seeds from which smart solutions grow.

## Features

- **`extract_kwargs`** - Decorator for extracting and grouping keyword arguments by prefix
- **`SmartOptions`** - Intelligent options merging with filtering and defaults
- **Three flexible styles** - Prefix style, dict style, and boolean activation
- **Zero dependencies** - Pure Python standard library only
- **Full type hints** - Complete typing support
- **Python 3.10+** - Modern Python

## Quick Example

```python
from smartseeds import extract_kwargs

@extract_kwargs(logging=True, cache=True)
def setup_service(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
    print(f"Logging config: {logging_kwargs}")
    print(f"Cache config: {cache_kwargs}")

# All these styles work:
setup_service(
    name="api",
    logging_level="INFO",      # → logging_kwargs={'level': 'INFO'}
    cache_ttl=300,             # → cache_kwargs={'ttl': 300}
)

setup_service(
    name="api",
    logging={'level': 'INFO'},  # Dict style
    cache=True                  # Boolean activation
)
```

## Documentation

```{toctree}
:maxdepth: 2
:caption: Getting Started

user-guide/installation
user-guide/quickstart
```

```{toctree}
:maxdepth: 2
:caption: User Guide

user-guide/extract-kwargs
user-guide/smart-options
user-guide/best-practices
```

```{toctree}
:maxdepth: 2
:caption: Examples

examples/index
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/reference
```

```{toctree}
:maxdepth: 2
:caption: Appendix

appendix/architecture
appendix/contributing
```

## Part of Genro-Libs

SmartSeeds is part of the [Genro-Libs](https://github.com/softwell/genro-libs) ecosystem.

## License

MIT License - Copyright © 2025 Genropy Team
