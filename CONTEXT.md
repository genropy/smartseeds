# SmartSeeds Context - Extract Kwargs Pattern

## What is SmartSeeds?

**SmartSeeds** è una libreria di utilities condivise per l'ecosistema smart* (smartroute, smartasync, etc.).

**Motto**: "Essential utilities that grow smart solutions" 🌱

**Caratteristiche**:
- Zero dipendenze esterne
- Python puro (3.10+)
- Utilities riusabili tra i vari progetti smart*

## Current Focus: extract_kwargs Decorator

### Purpose

Il decorator `extract_kwargs` risolve un problema comune nei progetti Genropy: la gestione di parametri con prefisso che devono essere passati a funzioni/oggetti nested.

### Problem It Solves

Quando una funzione deve accettare parametri per oggetti che crea internamente, ci sono due approcci tradizionali:

**Approccio 1: Parametri espliciti** (verboso)
```python
def connect(host, port, logging_level=None, logging_format=None, logging_file=None):
    logger = Logger(level=logging_level, format=logging_format, file=logging_file)
```

**Approccio 2: **kwargs catch-all** (poco chiaro)
```python
def connect(host, port, **kwargs):
    # Non si sa quali kwargs sono validi
    logger = Logger(**kwargs)  # Passa tutto, anche parametri non pertinenti
```

### Solution: extract_kwargs

Il decorator `extract_kwargs` permette tre stili di chiamata equivalenti:

#### Style 1: Prefix Style (most explicit)
```python
@extract_kwargs(logging=None)
def connect(host, port, logging_kwargs=None):
    if logging_kwargs:
        logger = Logger(**logging_kwargs)

# Usage
connect('localhost', 8000, logging_level='INFO', logging_format='json')
# → logging_kwargs = {'level': 'INFO', 'format': 'json'}
```

#### Style 2: Dict Style (compact)
```python
@extract_kwargs(logging=None)
def connect(host, port, logging_kwargs=None):
    if logging_kwargs:
        logger = Logger(**logging_kwargs)

# Usage
connect('localhost', 8000, logging={'level': 'INFO', 'format': 'json'})
# → logging_kwargs = {'level': 'INFO', 'format': 'json'}
```

#### Style 3: Boolean Activation (defaults)
```python
@extract_kwargs(logging=None)
def connect(host, port, logging_kwargs=None):
    if logging_kwargs:
        logger = Logger(**logging_kwargs)

# Usage
connect('localhost', 8000, logging=True)
# → logging_kwargs = {} (empty dict for defaults)
```

### How It Works

1. **Decorator Parameters**: `@extract_kwargs(logging=None, async_config=None)`
   - Keys define extraction prefixes
   - Values are defaults (not used in current implementation)

2. **Function Signature**: Decorated function MUST have `{prefix}_kwargs` parameters
   ```python
   def my_func(logging_kwargs=None, async_config_kwargs=None):
   ```

3. **Runtime Extraction**:
   - Cerca `{prefix}_` in kwargs → raccoglie in `{prefix}_kwargs`
   - Cerca `{prefix}` dict in kwargs → merge in `{prefix}_kwargs`
   - Rimuove parametri processati da kwargs
   - Passa `{prefix}_kwargs` alla funzione

### Real-World Usage: SmartSwitch

```python
from smartseeds import extract_kwargs

class Switcher:
    @extract_kwargs(logging=None, async_config=None)
    def __init__(self, logging_kwargs=None, async_config_kwargs=None):
        if logging_kwargs:
            self.logger = LoggingPlugin(**logging_kwargs)
        if async_config_kwargs:
            self.async_handler = AsyncPlugin(**async_config_kwargs)

# All these work:
sw = Switcher(logging_level='DEBUG', logging_mode='silent')
sw = Switcher(logging={'level': 'DEBUG', 'mode': 'silent'})
sw = Switcher(logging=True)  # Use defaults
```

### Implementation Requirements

**File**: `src/smartseeds/decorators.py`

```python
from functools import wraps
from typing import Any, Callable

def extract_kwargs(**extract_specs: Any) -> Callable:
    """
    Decorator to extract and group keyword arguments by prefix.

    Args:
        **extract_specs: Keys are prefixes to extract, values are defaults

    Example:
        @extract_kwargs(logging=None)
        def func(logging_kwargs=None):
            pass

        func(logging_level='INFO')  # → logging_kwargs={'level': 'INFO'}
        func(logging={'level': 'INFO'})  # → logging_kwargs={'level': 'INFO'}
        func(logging=True)  # → logging_kwargs={}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for extract_key, extract_value in extract_specs.items():
                grp_key = f'{extract_key}_kwargs'

                # Start with existing {prefix}_kwargs or empty dict
                current = kwargs.pop(grp_key, None) or {}

                # Style 2: Dict style - logging={'level': 'INFO'}
                if extract_key in kwargs:
                    prefix_value = kwargs.pop(extract_key)
                    if isinstance(prefix_value, dict):
                        current.update(prefix_value)
                    elif prefix_value is True:
                        # Style 3: Boolean - logging=True
                        pass  # Keep empty dict for defaults

                # Style 1: Prefix style - logging_level='INFO'
                prefix = f'{extract_key}_'
                keys_to_process = list(kwargs.keys())
                for key in keys_to_process:
                    if key.startswith(prefix):
                        param_name = key[len(prefix):]
                        current[param_name] = kwargs.pop(key)

                # Set result (None if empty)
                kwargs[grp_key] = current if current else None

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Test Requirements

**File**: `tests/test_decorators.py`

Key test cases:
1. **Prefix style**: `func(logging_level='INFO')` → `{'level': 'INFO'}`
2. **Dict style**: `func(logging={'level': 'INFO'})` → `{'level': 'INFO'}`
3. **Boolean activation**: `func(logging=True)` → `{}`
4. **Multiple prefixes**: `func(logging_level='INFO', async_timeout=30)` → both extracted
5. **Mixed styles**: `func(logging={'level': 'INFO'}, logging_mode='silent')` → merged
6. **No extraction**: `func()` → `logging_kwargs=None`
7. **Cleanup**: Extracted params removed from kwargs

### Integration with smartroute

SmartRoute usa `extract_kwargs` per plugin configuration:

```python
from smartseeds import extract_kwargs

class Service:
    @extract_kwargs(logging=None)
    def __init__(self, logging_kwargs=None):
        if logging_kwargs:
            self.register_plugin(LoggingPlugin, **logging_kwargs)

# Users can choose their preferred style:
svc = Service(logging_level='DEBUG', logging_mode='silent')  # Explicit
svc = Service(logging={'level': 'DEBUG', 'mode': 'silent'})  # Compact
svc = Service(logging=True)  # Defaults
```

## Current Status

**Structure**:
- ✅ `pyproject.toml` configured
- ✅ `src/smartseeds/__init__.py` exports
- ✅ `src/smartseeds/decorators.py` implementation started
- ✅ `tests/test_decorators.py` test suite created
- ⏳ Tests need verification and fixes

**Dependencies**: NONE (stdlib only)

**Python**: 3.10+

**License**: MIT

## Next Steps

1. Run tests: `pytest tests/test_decorators.py -v`
2. Fix any test failures
3. Verify all three styles work correctly
4. Check edge cases (empty dicts, None values, etc.)
5. Document behavior in docstrings

## Important Notes

- **DO NOT** include `Bag` class in current work (user explicitly excluded it)
- Focus ONLY on `extract_kwargs` decorator
- Maintain zero dependencies
- Follow existing Genropy patterns
- All tests must pass before considering complete

## References

- **SmartSwitch**: Uses extract_kwargs for plugin configuration
- **Genropy**: Original implementation reference
- **Project**: `/Users/gporcari/Sviluppo/genro_ng/meta-genro-libs/sub-projects/smartseeds/`

---

**Author**: Giovanni Porcari <softwell@softwell.it>
**Created**: 2025-11-11
**Purpose**: Context for Claude to work on extract_kwargs implementation
