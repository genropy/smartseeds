# Installation

SmartSeeds is a Python package that can be installed via pip.

## Requirements

- Python 3.10 or higher
- No external dependencies (pure Python standard library)

## Install from PyPI

```bash
pip install smartseeds
```

## Install from Source

For development or to get the latest changes:

```bash
git clone https://github.com/genropy/smartseeds.git
cd smartseeds
pip install -e ".[dev]"
```

## Verify Installation

```python
import smartseeds
print(smartseeds.__version__)
# Output: 0.1.0

from smartseeds import extract_kwargs
print(extract_kwargs.__doc__)
```

## Optional Dependencies

### Development

For running tests and linting:

```bash
pip install smartseeds[dev]
```

This installs:
- pytest (testing)
- pytest-cov (coverage)
- ruff (linting)
- black (formatting)
- mypy (type checking)

### Documentation

For building documentation:

```bash
pip install smartseeds[docs]
```

This installs:
- sphinx
- sphinx-rtd-theme
- sphinx-autodoc-typehints
- myst-parser
- sphinxcontrib-mermaid

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [extract_kwargs Guide](extract-kwargs.md) - Learn the decorator in detail
- [Best Practices](best-practices.md) - Production usage patterns
