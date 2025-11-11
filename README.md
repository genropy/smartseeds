# SmartSeeds 🌱

**Essential utilities that grow smart solutions**

SmartSeeds is a lightweight, zero-dependency Python library providing core utilities for the smart* ecosystem (smartswitch, smartasync, etc.). Think of it as the seeds from which smart solutions grow.

[![Part of Genro-Libs](https://img.shields.io/badge/Part%20of-Genro--Libs-blue.svg)](https://github.com/softwell/genro-libs)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/smartseeds.svg)](https://badge.fury.io/py/smartseeds)

## Features

- **`extract_kwargs`**: Decorator for extracting and grouping keyword arguments by prefix
- **`dictExtract`**: Utility for extracting values from dictionaries with prefix matching
- **`Bag`**: Dictionary with attribute access (`bag.key` instead of `bag['key']`)
- **Zero dependencies**: Pure Python standard library

## Installation

```bash
pip install smartseeds
```

## Quick Start

### extract_kwargs Decorator

Extract kwargs by prefix into separate parameter groups:

```python
from smartseeds import extract_kwargs

@extract_kwargs(logging=True, cache=True)
def setup_service(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
    print(f"Logging config: {logging_kwargs}")
    print(f"Cache config: {cache_kwargs}")
    print(f"Other: {kwargs}")

# All these work:
setup_service(
    name="api",
    logging_level="INFO",      # → logging_kwargs={'level': 'INFO'}
    logging_format="json",     # → logging_kwargs={'format': 'json'}
    cache_ttl=300,             # → cache_kwargs={'ttl': 300}
    timeout=30                 # → kwargs={'timeout': 30}
)

# Or use dict style:
setup_service(
    name="api",
    logging={'level': 'INFO', 'format': 'json'},
    cache={'ttl': 300}
)
```

### Bag - Dict with Attribute Access

```python
from smartseeds import Bag

config = Bag(host='localhost', port=8000)
print(config.host)  # → 'localhost'
print(config.port)  # → 8000

# Works like a dict too
print(config['host'])  # → 'localhost'
config['timeout'] = 30
```

### dictExtract Utility

```python
from smartseeds import dictExtract

params = {
    'api_host': 'localhost',
    'api_port': 8000,
    'db_name': 'mydb',
    'timeout': 30
}

# Extract all api_* parameters
api_config = dictExtract(params, 'api_', slice_prefix=True, pop=True)
# → {'host': 'localhost', 'port': 8000}
# params now: {'db_name': 'mydb', 'timeout': 30}
```

## Use in smart* Ecosystem

SmartSeeds is designed to be used by other smart* tools:

```python
# In smartswitch, smartasync, etc.
from smartseeds import extract_kwargs

class Switcher:
    @extract_kwargs(logging=True, async_mode=True)
    def __init__(self, name=None, logging_kwargs=None, async_kwargs=None, **kwargs):
        # Plugin configuration extracted automatically
        if logging_kwargs:
            self.plug('logging', **logging_kwargs)
        if async_kwargs:
            self.plug('async', **async_kwargs)
```

## Documentation

Full documentation available at: https://smartseeds.readthedocs.io

## Part of the Smart* Family

SmartSeeds is part of the Genropy smart* toolkit:

- [smartswitch](https://github.com/genropy/smartswitch) - Rule-based function dispatch
- [smartasync](https://github.com/genropy/smartasync) - Async utilities
- [smartpub](https://github.com/genropy/smartpub) - Pub/sub messaging

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.
