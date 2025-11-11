"""Tests for extract_kwargs decorator."""

import pytest
from smartseeds import extract_kwargs


class TestExtractKwargsBasic:
    """Basic extract_kwargs functionality."""

    def test_extract_with_prefix(self):
        """Test extracting kwargs with prefix."""
        @extract_kwargs(logging=True)
        def func(name, logging_kwargs=None, **kwargs):
            return {"logging": logging_kwargs, "other": kwargs}

        result = func(name="test", logging_level="INFO", logging_format="json", timeout=30)

        assert result["logging"] == {"level": "INFO", "format": "json"}
        assert result["other"] == {"timeout": 30}

    def test_extract_multiple_prefixes(self):
        """Test extracting multiple prefix groups."""
        @extract_kwargs(logging=True, cache=True)
        def func(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
            return {"logging": logging_kwargs, "cache": cache_kwargs, "other": kwargs}

        result = func(
            name="test",
            logging_level="INFO",
            cache_ttl=300,
            cache_backend="redis",
            timeout=30
        )

        assert result["logging"] == {"level": "INFO"}
        assert result["cache"] == {"ttl": 300, "backend": "redis"}
        assert result["other"] == {"timeout": 30}

    def test_dict_style(self):
        """Test passing kwargs as dict."""
        @extract_kwargs(logging=True)
        def func(name, logging_kwargs=None, **kwargs):
            return {"logging": logging_kwargs, "other": kwargs}

        result = func(
            name="test",
            logging={"level": "INFO", "format": "json"},
            timeout=30
        )

        assert result["logging"] == {"level": "INFO", "format": "json"}
        assert result["other"] == {"timeout": 30}

    def test_mixed_style(self):
        """Test mixing dict and prefix styles."""
        @extract_kwargs(logging=True, cache=True)
        def func(name, logging_kwargs=None, cache_kwargs=None, **kwargs):
            return {"logging": logging_kwargs, "cache": cache_kwargs, "other": kwargs}

        result = func(
            name="test",
            logging={"level": "INFO"},
            cache_ttl=300,
            timeout=30
        )

        assert result["logging"] == {"level": "INFO"}
        assert result["cache"] == {"ttl": 300}
        assert result["other"] == {"timeout": 30}

    def test_no_extracted_kwargs(self):
        """Test when no kwargs match prefix."""
        @extract_kwargs(logging=True)
        def func(name, logging_kwargs=None, **kwargs):
            return {"logging": logging_kwargs, "other": kwargs}

        result = func(name="test", timeout=30)

        assert result["logging"] is None
        assert result["other"] == {"timeout": 30}

    def test_boolean_activation(self):
        """Test boolean activation (logging=True)."""
        @extract_kwargs(logging=True)
        def func(name, logging_kwargs=None, **kwargs):
            return {"logging": logging_kwargs}

        result = func(name="test", logging=True)

        assert result["logging"] == {}  # Activated but no params
