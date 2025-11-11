# LLM.md - SmartSeeds

**AI Assistant Context for SmartSeeds Development**

## Project Overview

**SmartSeeds** is a zero-dependency Python library providing the `extract_kwargs` decorator for the smart* ecosystem (smartswitch, smartcache, etc.).

**Repository**: https://github.com/genropy/smartseeds
**Part of**: [Genro-Libs Toolkit](https://github.com/softwell/genro-libs)
**License**: MIT
**Python**: 3.8+

## Core Purpose

SmartSeeds provides **ONE primary feature**:

### extract_kwargs Decorator

Extracts and groups keyword arguments by prefix into separate parameter families.

**Example**:
```python
from smartseeds import extract_kwargs

@extract_kwargs(logging=True, cache=True)
def setup(logging_kwargs=None, cache_kwargs=None):
    print(f"Logging: {logging_kwargs}")
    print(f"Cache: {cache_kwargs}")

# Call with prefixed params
setup(
    logging_level="DEBUG",
    logging_file="app.log",
    cache_ttl=300,
    cache_backend="redis"
)
# Output:
# Logging: {'level': 'DEBUG', 'file': 'app.log'}
# Cache: {'ttl': 300, 'backend': 'redis'}
```

## Project Scope

### ✅ IN SCOPE (Public API)

- `extract_kwargs` decorator ONLY
- Three calling styles (prefix, dict, boolean)
- Full type hints
- Zero dependencies

### ❌ OUT OF SCOPE (Not Public)

- `dictExtract` - Internal utility only
- `Bag` class - Removed from this project
- Other dict utilities - Not part of SmartSeeds

**IMPORTANT**: User explicitly stated "per ora mi serve solo extract kwargs" - do NOT add other utilities to public API.

## Key Design Decisions

### 1. Backwards Compatibility

**CRITICAL**: The implementation MUST maintain 100% backwards compatibility with original Genropy `extract_kwargs`.

User requirement: "non devo rompere col passato"

The current implementation was tested against the original with comprehensive compatibility tests (all passing).

### 2. Internal vs Public

- `dictExtract` is **internal** utility in `dict_utils.py`
- Only `extract_kwargs` is exported from `__init__.py`
- Tests focus on public API behavior

### 3. Zero Dependencies

**Philosophy**: SmartSeeds uses ONLY Python standard library:
- `functools.wraps`
- `typing`
- No external packages

## Project Structure

```
smartseeds/
├── src/smartseeds/
│   ├── __init__.py          # Exports: extract_kwargs only
│   ├── decorators.py        # Main decorator implementation
│   └── dict_utils.py        # Internal: dictExtract utility
│
├── tests/
│   └── test_decorators.py   # 10 tests, 96% coverage
│
├── docs/                    # Sphinx documentation
│   ├── conf.py
│   ├── index.md
│   ├── user-guide/
│   ├── examples/
│   ├── api/
│   └── appendix/
│
├── genropy_comparison/      # Private, git-ignored
│   └── IMPLEMENTATION_COMPARISON.md
│
├── pyproject.toml
├── LICENSE                  # MIT
├── README.md
└── LLM.md                   # This file
```

## Testing

### Current Status

- **Tests**: 10 tests in `test_decorators.py`
- **Coverage**: 96% (only defensive unreachable code missing)
- **All tests passing**: ✅

### Test Organization

```python
class TestExtractKwargsBasic:
    """Core functionality - 4 tests"""

class TestExtractKwargsOptions:
    """Advanced options - 3 tests"""

class TestExtractKwargsEdgeCases:
    """Edge cases - 3 tests"""
```

### Running Tests

```bash
pytest                                    # All tests
pytest --cov=smartseeds                  # With coverage
pytest --cov=smartseeds --cov-report=html  # HTML report
```

## Documentation

### Format

- **Tool**: Sphinx with MyST Markdown
- **Theme**: sphinx_rtd_theme (Read the Docs)
- **Extensions**: autodoc, napoleon, intersphinx, mermaid

### Standards

Following **Genro documentation standards**:

1. **Test-first**: Examples extracted from tests
2. **Test anchors**: `<!-- test: test_file.py::test_function -->`
3. **GitHub links**: Link to actual test code
4. **Comprehensive**: User guide, examples, API, appendix

### Building Docs

```bash
cd docs
sphinx-build -b html . _build/html
```

## Common Tasks

### Add New Feature

1. **Write tests first** in `test_decorators.py`
2. **Implement** in `decorators.py`
3. **Update docs** with test anchors
4. **Run tests**: `pytest --cov=smartseeds`
5. **Check coverage**: Must stay ≥95%

### Update Documentation

1. **Update/add tests** if needed
2. **Add test anchors** to docs
3. **Add GitHub links** to test code
4. **Build locally**: `sphinx-build -b html docs docs/_build/html`
5. **Check rendering**

### Release New Version

1. **Update version** in `src/smartseeds/__init__.py`
2. **Update CHANGELOG.md**
3. **Tag release**: `git tag v0.X.0`
4. **Push tag**: `git push origin v0.X.0`
5. **GitHub Actions** handles PyPI publish

## Important Files

### src/smartseeds/__init__.py

**Exports**: Only `extract_kwargs`

```python
from .decorators import extract_kwargs

__all__ = ["extract_kwargs"]
```

### src/smartseeds/decorators.py

**Main implementation** with:
- Full type hints (`TypeVar`, `Callable`, etc.)
- `@wraps` for metadata preservation
- Support for methods and functions
- Optional adapter calling
- Three extraction styles

### src/smartseeds/dict_utils.py

**Internal utility** for prefix extraction:
- `dictExtract(mydict, prefix, pop, slice_prefix, is_list)`
- **Not exported** from package
- Used by `extract_kwargs` internally

## Git Workflow

### Branches

- `main` - Production branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation

### Commits

Use **conventional commits**:
```
feat: add new extraction option
fix: handle missing adapter gracefully
docs: update quickstart guide
test: add edge case for empty kwargs
```

### CI/CD

**GitHub Actions workflows**:
- `.github/workflows/test.yml` - Tests on push/PR
- `.github/workflows/docs.yml` - Build docs on push to main
- `.github/workflows/publish.yml` - Publish to PyPI on tag

## Dependencies

### Runtime

**NONE** - Zero dependencies

### Development

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=2.0.0",
    "myst-parser>=2.0.0",
    "sphinxcontrib-mermaid>=0.9.0",
]
```

## Key Concepts

### Three Calling Styles

1. **Prefix style** (most common):
   ```python
   setup(logging_level="DEBUG", logging_file="app.log")
   # → logging_kwargs = {'level': 'DEBUG', 'file': 'app.log'}
   ```

2. **Dict style** (bulk config):
   ```python
   setup(logging={'level': 'DEBUG', 'file': 'app.log'})
   # → logging_kwargs = {'level': 'DEBUG', 'file': 'app.log'}
   ```

3. **Boolean activation** (empty dict):
   ```python
   setup(logging=True)
   # → logging_kwargs = {}
   ```

### Extraction Options

- `pop=True` (default for `param=True`): Remove from kwargs
- `pop=False` (default for `param={...}`): Keep in kwargs
- `slice_prefix=True` (default): Remove prefix from keys
- `is_list=False` (default): Not implemented yet

### Adapter Pattern

Optional adapter method for pre-processing:

```python
class Service:
    def _normalize_config(self, kwargs):
        """Called before extraction."""
        # Normalize or validate kwargs
        pass

    @extract_kwargs(_adapter='_normalize_config', logging=True)
    def __init__(self, logging_kwargs=None):
        pass
```

## Troubleshooting

### Tests Failing

```bash
# Run with verbose output
pytest -vv

# Run specific test
pytest tests/test_decorators.py::TestExtractKwargsBasic::test_extract_with_prefix

# Check coverage
pytest --cov=smartseeds --cov-report=term-missing
```

### Coverage Dropped

- Check which lines are missing: `pytest --cov=smartseeds --cov-report=term-missing`
- Add tests for uncovered code
- Aim for ≥95% coverage

### Documentation Build Fails

```bash
# Check for errors
sphinx-build -b html docs docs/_build/html -W

# Common issues:
# - Missing MyST markdown extension
# - Invalid rst/markdown syntax
# - Missing intersphinx mappings
```

## Related Projects

**Genro-Libs Ecosystem**:
- **smartswitch** - Uses `extract_kwargs` for plugin configuration
- **gtext** - Template generation tool
- **genro-libs** - Meta-repository (private)

**Integration Example** (smartswitch):
```python
from smartseeds import extract_kwargs

class Switcher:
    @extract_kwargs(logging=True, plugins=True)
    def __init__(self, name, logging_kwargs=None, plugins_kwargs=None):
        if logging_kwargs:
            self.setup_logging(**logging_kwargs)
        if plugins_kwargs:
            self.register_plugins(plugins_kwargs)
```

## User Feedback History

Key feedback that shaped the project:

1. **"per ora mi serve solo extract kwargs"** - Removed Bag and dictExtract from public API
2. **"non devo rompere col passato"** - Maintain backwards compatibility
3. **"tieni solo la nuova emettila in decorators"** - Use improved v2 as main implementation
4. **"il confronto lo metti in un folder non pubblico"** - Keep comparison private
5. **"si"** - Proceed with comprehensive documentation

## For AI Assistants

When working on SmartSeeds:

1. **Always read tests first** - Tests define behavior
2. **Maintain backwards compatibility** - User requirement
3. **Only export extract_kwargs** - No other public utilities
4. **Zero dependencies** - Use only standard library
5. **Test-first documentation** - Extract from actual tests
6. **95%+ coverage** - Maintain high test coverage
7. **Conventional commits** - Use feat/fix/docs prefixes

## Quick Reference

```bash
# Development
pip install -e ".[dev,docs]"
pytest --cov=smartseeds

# Documentation
sphinx-build -b html docs docs/_build/html

# Release (maintainers)
# 1. Update __version__ in __init__.py
# 2. git tag v0.X.0
# 3. git push origin v0.X.0
```

---

**Last Updated**: 2025-11-11
**Maintained By**: Genropy Team
**Contact**: https://github.com/genropy/smartseeds/issues
