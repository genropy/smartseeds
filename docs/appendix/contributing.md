# Contributing

Guidelines for contributing to SmartSeeds.

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/genropy/smartseeds.git
cd smartseeds
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev,docs]"
```

This installs:
- Core package in editable mode
- Testing tools (pytest, pytest-cov)
- Documentation tools (Sphinx, MyST)

### 4. Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=smartseeds --cov-report=html
```

## Project Structure

```
smartseeds/
├── src/smartseeds/          # Source code
│   ├── __init__.py          # Public API
│   ├── decorators.py        # extract_kwargs implementation
│   └── dict_utils.py        # Internal utilities
│
├── tests/                   # Test suite
│   └── test_decorators.py   # All tests
│
├── docs/                    # Sphinx documentation
│   ├── conf.py              # Sphinx config
│   ├── index.md             # Landing page
│   ├── user-guide/          # User guides
│   ├── examples/            # Examples
│   ├── api/                 # API reference
│   └── appendix/            # Additional info
│
├── pyproject.toml           # Project metadata
├── LICENSE                  # MIT license
└── README.md                # Project overview
```

## Coding Standards

### Python Style

Follow **PEP 8** with these specifics:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces
- **Quotes**: Single quotes for strings (except docstrings)
- **Type hints**: Required for all public functions

### Type Hints

All public functions **must have type hints**:

```python
from typing import Optional, Dict, Any, Callable

def extract_kwargs(
    _adapter: Optional[str] = None,
    _dictkwargs: Optional[Dict[str, Any]] = None,
    **extraction_specs: Any
) -> Callable[[F], F]:
    """Decorator that extracts kwargs."""
    ...
```

### Docstrings

Use **Google style** docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Short description.

    Longer description with more details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Example:
        >>> my_function("test", 42)
        True
    """
    ...
```

## Testing Guidelines

### Test Organization

Tests are organized by concern:

```python
class TestExtractKwargsBasic:
    """Basic extract_kwargs functionality."""

    def test_extract_with_prefix(self):
        """Test extracting kwargs with prefix."""
        ...

class TestExtractKwargsOptions:
    """Advanced options."""

    def test_pop_option(self):
        """Test pop=True removes params."""
        ...
```

### Test Requirements

Every contribution should:

1. **Add tests** for new features
2. **Update tests** for changed behavior
3. **Maintain 95%+ coverage**
4. **Pass all existing tests**

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_decorators.py

# Run specific test
pytest tests/test_decorators.py::TestExtractKwargsBasic::test_extract_with_prefix

# With coverage
pytest --cov=smartseeds --cov-report=term-missing
```

## Documentation

### Building Docs Locally

```bash
cd docs
sphinx-build -b html . _build/html
```

View at `docs/_build/html/index.html`.

### Documentation Standards

1. **Test-first**: Extract examples from tests
2. **Test anchors**: Add `<!-- test: ... -->` comments
3. **GitHub links**: Link to actual test code
4. **MyST Markdown**: Use MyST extensions

Example:

```markdown
<!-- test: test_decorators.py::TestExtractKwargsBasic::test_extract_with_prefix -->

Basic usage example:

[From test](https://github.com/genropy/smartseeds/blob/main/tests/test_decorators.py#L18-L25)

\`\`\`python
@extract_kwargs(logging=True)
def my_function(logging_kwargs=None):
    print(logging_kwargs)
\`\`\`
```

## Pull Request Process

### 1. Create Branch

```bash
git checkout -b feature/your-feature-name
```

Use prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring

### 2. Make Changes

- Write code
- Add tests
- Update docs
- Run tests locally

### 3. Commit

Use **conventional commits**:

```bash
git commit -m "feat: add support for nested extraction"
git commit -m "fix: handle missing adapter methods"
git commit -m "docs: update quickstart guide"
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Build/tooling

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub with:

1. **Clear title** - What does it do?
2. **Description** - Why is it needed?
3. **Test coverage** - How is it tested?
4. **Breaking changes** - Any breaking changes?

### 5. Review Process

- **CI checks** must pass
- **Code review** by maintainer
- **Coverage** must not decrease
- **Docs** must be updated

## Release Process

(For maintainers only)

### Pre-Release Checklist

**CRITICAL**: Before creating a release, verify ALL version numbers are synchronized:

```bash
# 1. Check __init__.py version
grep "__version__" src/smartseeds/__init__.py

# 2. Check pyproject.toml version
grep "^version" pyproject.toml

# 3. Both MUST match! If not, build will publish wrong version
```

### Step-by-Step Release Process

#### 1. Update Version Numbers

**IMPORTANT**: Update version in BOTH files:

**File 1: `src/smartseeds/__init__.py`**
```python
__version__ = "0.2.0"
```

**File 2: `pyproject.toml`**
```toml
[project]
name = "smartseeds"
version = "0.2.0"  # ← MUST match __init__.py
```

#### 2. Update Changelog

Add release notes to `CHANGELOG.md`:

```markdown
## [0.2.0] - 2025-11-16

### Added
- New feature X
- Support for Y

### Fixed
- Bug in Z
```

#### 3. Commit Version Updates

```bash
git add src/smartseeds/__init__.py pyproject.toml CHANGELOG.md
git commit -m "build: bump version to 0.2.0"
git push origin main
```

#### 4. Create and Push Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0: Brief description"

# Push tag (triggers CI/CD)
git push origin v0.2.0
```

#### 5. Verify Build

After pushing the tag:

1. **Check GitHub Actions**: Verify workflow completes successfully
2. **Check build logs**: Confirm correct version was built
   ```bash
   gh run list --limit 1
   gh run view <run-id> --log | grep "creating smartseeds"
   # Should see: "creating smartseeds-0.2.0"
   ```
3. **Check PyPI**: Verify correct version was published
   ```bash
   pip index versions smartseeds
   # Should see: "Available versions: 0.2.0, ..."
   ```

### Troubleshooting Releases

#### Wrong Version Published

If wrong version was published:

1. **Delete the tag**:
   ```bash
   git tag -d v0.2.0
   git push origin :refs/tags/v0.2.0
   ```

2. **Fix version in both files**:
   - `src/smartseeds/__init__.py`
   - `pyproject.toml`

3. **Commit, recreate tag, and push**:
   ```bash
   git add src/smartseeds/__init__.py pyproject.toml
   git commit -m "build: fix version to 0.2.0"
   git push origin main
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

#### Release Failed

If GitHub Actions workflow fails:

1. Check workflow logs: `gh run view <run-id> --log`
2. Fix the issue
3. Delete and recreate the tag (see above)

### Version Management Best Practices

1. **Always update both version locations** (`__init__.py` and `pyproject.toml`)
2. **Verify versions match** before pushing tag
3. **Use annotated tags** (`-a` flag) for releases
4. **Check build logs** to confirm correct version
5. **Never skip verification** - it catches mistakes early

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/genropy/smartseeds/issues)
- **Discussions**: [GitHub Discussions](https://github.com/genropy/smartseeds/discussions)
- **Email**: Contact maintainers (see README)

## Code of Conduct

### Our Standards

- **Be respectful** - Treat everyone with respect
- **Be constructive** - Provide helpful feedback
- **Be inclusive** - Welcome all contributors
- **Be patient** - We all started somewhere

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Unprofessional conduct

## License

By contributing to SmartSeeds, you agree that your contributions will be licensed under the **MIT License**.

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Documentation (for major contributions)

Thank you for contributing! 🌱

## See Also

- [Architecture](architecture.md) - Technical design
- [Best Practices](../user-guide/best-practices.md) - Usage patterns
- [API Reference](../api/reference.md) - Complete API
