# LLM.md - SmartSeeds

**AI Assistant Context for SmartSeeds Development**

## Project Overview

**SmartSeeds** is a zero-dependency Python library providing essential utilities for the smart* ecosystem (smartroute, smartasync, etc.):
- `extract_kwargs` decorator for grouping keyword arguments
- `smartsuper` decorator for automatic parent method calling
- `SmartOptions` for intelligent option merging

**Repository**: https://github.com/genropy/smartseeds
**Part of**: [Genro-Libs Toolkit](https://github.com/softwell/genro-libs)
**License**: MIT
**Python**: 3.10+

## Core Features

SmartSeeds provides **three primary features**:

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

### smartsuper Decorator

Automatically calls parent class methods before or after the decorated method. Supports three usage modes:

**Example**:
```python
from smartseeds import smartsuper

# Mode 1: Method decorator (BEFORE)
class Derived(Base):
    @smartsuper
    def setup(self):
        print("Derived setup")  # Base.setup() called BEFORE this

# Mode 2: Method decorator (AFTER)
class Derived(Base):
    @smartsuper.after
    def cleanup(self):
        print("Derived cleanup")  # Base.cleanup() called AFTER this

# Mode 3: Class decorator (auto-decorates ALL overrides)
@smartsuper
class Derived(Base):
    def foo(self): pass  # Auto-decorated as BEFORE

    @smartsuper.after  # Explicit AFTER takes precedence
    def bar(self): pass
```

**Key Features**:
- Uses `__new__` to detect class vs method decoration
- Magic methods (`__dunder__`) are NOT auto-decorated for safety
- Explicit decoration of magic methods still possible
- Uses descriptor protocol (`__set_name__`, `__get__`)
- `__smartsuper_mode__` attribute marks methods as "before" or "after"

### SmartOptions

Intelligent option merging with filtering support.

**Example**:
```python
from smartseeds import SmartOptions

opts = SmartOptions(
    incoming={'timeout': 10, 'retries': None},
    defaults={'timeout': 5, 'retries': 3},
    ignore_none=True  # Skip None values from incoming
)
print(opts.timeout)  # 10 (from incoming)
print(opts.retries)  # 3 (from defaults, None ignored)
```

## Project Scope

### ✅ IN SCOPE (Public API)

- `extract_kwargs` decorator - Group kwargs by prefix
- `smartsuper` decorator - Automatic parent method calling
- `SmartOptions` class - Intelligent option merging
- Three calling styles for extract_kwargs (prefix, dict, boolean)
- Full type hints
- Zero dependencies

### ❌ OUT OF SCOPE (Internal/Private)

- `dictExtract` - Internal utility only
- `filtered_dict`, `make_opts` - Internal helpers
- `Bag` class - Removed from this project

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
│   ├── __init__.py          # Exports: extract_kwargs, smartsuper, SmartOptions
│   ├── decorators.py        # extract_kwargs and smartsuper decorators
│   └── dict_utils.py        # SmartOptions and internal helpers
│
├── tests/
│   ├── test_decorators.py   # extract_kwargs tests (12 tests)
│   ├── test_super.py        # smartsuper tests (24 tests)
│   └── test_dict_utils.py   # SmartOptions tests (15 tests)
│   # Total: 51 tests, 98% coverage
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

- **Total Tests**: 51 tests across 3 test files
- **Coverage**: 98% total
  - `__init__.py`: 100%
  - `dict_utils.py`: 100%
  - `decorators.py`: 97% (3 lines defensive code)
- **All tests passing**: ✅

### Test Organization

**test_decorators.py** (12 tests):
```python
class TestExtractKwargsBasic:
    """Core functionality - 4 tests"""

class TestExtractKwargsOptions:
    """Advanced options - 3 tests"""

class TestExtractKwargsEdgeCases:
    """Edge cases - 5 tests"""
```

**test_super.py** (24 tests):
```python
class TestSmartSuperDecorator:
    """Method decorator (BEFORE) - 6 tests"""

class TestSmartSuperAfterDecorator:
    """Method decorator (AFTER) - 5 tests"""

class TestSmartSuperEdgeCases:
    """Edge cases - 3 tests"""

class TestSmartSuperAllDecorator:
    """Class decorator - 10 tests"""
```

**test_dict_utils.py** (15 tests):
```python
class TestFilteredDict:
    """filtered_dict helper - 3 tests"""

class TestMakeOpts:
    """make_opts helper - 6 tests"""

class TestSmartOptions:
    """SmartOptions class - 6 tests"""
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

**CRITICAL PRE-RELEASE CHECKLIST**

Before creating ANY release, you MUST verify version synchronization:

```bash
# 1. Check __init__.py version
grep "__version__" src/smartseeds/__init__.py

# 2. Check pyproject.toml version
grep "^version" pyproject.toml

# 3. BOTH MUST MATCH! If not, build will publish wrong version
```

**Why this matters**: The setuptools build process uses `pyproject.toml` as the authoritative source for package metadata. If `__init__.py` and `pyproject.toml` have different versions, PyPI will receive the version from `pyproject.toml`, NOT from `__init__.py`.

**Step-by-Step Release Process**:

1. **Update BOTH version locations**:
   ```bash
   # File 1: src/smartseeds/__init__.py
   __version__ = "0.X.0"

   # File 2: pyproject.toml
   version = "0.X.0"  # ← MUST match __init__.py
   ```

2. **Update CHANGELOG.md** with release notes

3. **Commit version updates**:
   ```bash
   git add src/smartseeds/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "build: bump version to 0.X.0"
   git push origin main
   ```

4. **Create and push annotated tag**:
   ```bash
   git tag -a v0.X.0 -m "Release v0.X.0: Brief description"
   git push origin v0.X.0
   ```

5. **Verify build**:
   ```bash
   # Check workflow ran successfully
   gh run list --limit 1

   # Check build logs show correct version
   gh run view <run-id> --log | grep "creating smartseeds"
   # Should see: "creating smartseeds-0.X.0"

   # Check PyPI shows correct version
   pip index versions smartseeds
   # Should see: "Available versions: 0.X.0, ..."
   ```

**If Wrong Version Published**:

1. Delete the tag:
   ```bash
   git tag -d v0.X.0
   git push origin :refs/tags/v0.X.0
   ```

2. Fix version in BOTH files (if not already correct)

3. Commit, recreate tag, and push:
   ```bash
   git add src/smartseeds/__init__.py pyproject.toml
   git commit -m "build: fix version to 0.X.0"
   git push origin main
   git tag -a v0.X.0 -m "Release v0.X.0"
   git push origin v0.X.0
   ```

**AI Assistant Notes**:
- ALWAYS check both version locations before proceeding
- NEVER skip the verification step
- If versions don't match, FIX before creating tag
- Use grep commands to verify, don't just read files visually

## Important Files

### src/smartseeds/__init__.py

**Public API Exports**:

```python
__version__ = "0.2.0"

from .decorators import extract_kwargs, smartsuper
from .dict_utils import SmartOptions

__all__ = [
    "extract_kwargs",
    "SmartOptions",
    "smartsuper",
]
```

### src/smartseeds/decorators.py

**Two main decorators**:

1. **extract_kwargs** (lines 19-119):
   - Full type hints (`TypeVar`, `Callable`, etc.)
   - `@wraps` for metadata preservation
   - Support for methods and functions
   - Optional adapter calling
   - Three extraction styles

2. **smartsuper** (lines 122-269):
   - Class-based descriptor using `__new__`, `__set_name__`, `__get__`
   - Detects class vs method decoration with `isinstance(target, type)`
   - `after` classmethod for AFTER behavior
   - `all` classmethod (explicit class decorator)
   - `_decorate_class` internal method for class decoration
   - `__smartsuper_mode__` attribute for tracking decoration type

### src/smartseeds/dict_utils.py

**Public class and internal helpers**:

1. **SmartOptions** (public):
   - Intelligent option merging with filtering
   - `ignore_none` and `ignore_empty` flags
   - `as_dict()` method for conversion
   - Dynamic attribute access via `__getattr__`, `__setattr__`, `__delattr__`

2. **Internal helpers** (not exported):
   - `dictExtract(mydict, prefix, pop, slice_prefix, is_list)` - Prefix extraction
   - `filtered_dict(source, filter_fn)` - Dict filtering
   - `make_opts(incoming, defaults, filter_fn, ignore_none, ignore_empty)` - Options factory

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
- **smartroute** - Uses `extract_kwargs` for plugin configuration
- **smartasync** - Async utilities
- **smartpublisher** - CLI/API framework based on SmartRoute
- **gtext** - Template generation tool
- **genro-libs** - Meta-repository (private)

**Integration Example** (smartroute):
```python
from smartseeds import extract_kwargs

class Service:
    @extract_kwargs(logging=True, plugins=True)
    def __init__(self, name, logging_kwargs=None, plugins_kwargs=None):
        if logging_kwargs:
            self.setup_logging(**logging_kwargs)
        if plugins_kwargs:
            self.register_plugins(plugins_kwargs)
```

## User Feedback History

Key feedback that shaped the project:

### v0.1.x - extract_kwargs
1. **"per ora mi serve solo extract kwargs"** - Initial focus on extract_kwargs only
2. **"non devo rompere col passato"** - Maintain backwards compatibility
3. **"tieni solo la nuova emettila in decorators"** - Use improved v2 as main implementation
4. **"il confronto lo metti in un folder non pubblico"** - Keep comparison private
5. **"si"** - Proceed with comprehensive documentation

### v0.2.0 - smartsuper and SmartOptions
6. **"ho pensato che sia meglio chiamarlo smartsuper"** - Renamed from `super` to avoid conflicts
7. **"ok fai cosi e togli i magic"** - Initial request to include magic methods
8. **"tu cosa consigli?"** - Asked for recommendation on magic methods
9. **"si"** - Agreed to exclude magic methods from class decorator for safety
10. **"arriva al 100"** - Push test coverage to 100% (achieved 98%)

## For AI Assistants

When working on SmartSeeds:

### General Guidelines
1. **Always read tests first** - Tests define behavior
2. **Zero dependencies** - Use only Python standard library
3. **Test-first documentation** - Extract examples from actual tests
4. **95%+ coverage** - Maintain high test coverage (currently 98%)
5. **Conventional commits** - Use feat/fix/docs prefixes

### Public API (v0.2.0)
- **extract_kwargs** - Decorator for grouping kwargs by prefix
- **smartsuper** - Decorator for automatic parent method calling
- **SmartOptions** - Class for intelligent option merging

### Internal Utilities (NOT public)
- `dictExtract`, `filtered_dict`, `make_opts` - Internal helpers only

### Key Implementation Details
- **extract_kwargs**: Maintains 100% backwards compatibility with Genropy original
- **smartsuper**: Uses `__new__` for universal class/method decoration, skips magic methods in class mode
- **SmartOptions**: Uses `SimpleNamespace`-like attribute access with filtering

## Quick Reference

```bash
# Development
pip install -e ".[dev,docs]"
pytest --cov=smartseeds

# Documentation
sphinx-build -b html docs docs/_build/html

# Release (maintainers) - MUST verify BOTH versions match first!
# 1. Check: grep "__version__" src/smartseeds/__init__.py
# 2. Check: grep "^version" pyproject.toml
# 3. Update BOTH files to same version
# 4. git commit -m "build: bump version to 0.X.0"
# 5. git tag -a v0.X.0 -m "Release v0.X.0"
# 6. git push origin main && git push origin v0.X.0
# 7. Verify: gh run view <id> --log | grep "creating smartseeds"
```

---

**Last Updated**: 2025-11-11
**Maintained By**: Genropy Team
**Contact**: https://github.com/genropy/smartseeds/issues
