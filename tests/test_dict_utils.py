"""Tests for dict utilities."""

import pytest
from smartseeds import dictExtract, Bag


class TestDictExtract:
    """Tests for dictExtract function."""

    def test_extract_with_slice(self):
        """Test extracting with prefix slicing."""
        source = {"api_host": "localhost", "api_port": 8000, "timeout": 30}
        result = dictExtract(source, "api_", slice_prefix=True, pop=False)

        assert result == {"host": "localhost", "port": 8000}
        assert source == {"api_host": "localhost", "api_port": 8000, "timeout": 30}

    def test_extract_with_pop(self):
        """Test extracting with pop (modifies source)."""
        source = {"api_host": "localhost", "api_port": 8000, "timeout": 30}
        result = dictExtract(source, "api_", slice_prefix=True, pop=True)

        assert result == {"host": "localhost", "port": 8000}
        assert source == {"timeout": 30}

    def test_extract_without_slice(self):
        """Test extracting without slicing prefix."""
        source = {"api_host": "localhost", "api_port": 8000, "timeout": 30}
        result = dictExtract(source, "api_", slice_prefix=False, pop=False)

        assert result == {"api_host": "localhost", "api_port": 8000}

    def test_no_matches(self):
        """Test when no keys match prefix."""
        source = {"timeout": 30, "retries": 3}
        result = dictExtract(source, "api_", slice_prefix=True, pop=False)

        assert result == {}
        assert source == {"timeout": 30, "retries": 3}


class TestBag:
    """Tests for Bag class."""

    def test_attribute_access(self):
        """Test accessing items via attributes."""
        bag = Bag(host="localhost", port=8000)

        assert bag.host == "localhost"
        assert bag.port == 8000

    def test_dict_access(self):
        """Test accessing items via dict keys."""
        bag = Bag(host="localhost", port=8000)

        assert bag["host"] == "localhost"
        assert bag["port"] == 8000

    def test_set_attribute(self):
        """Test setting items via attributes."""
        bag = Bag()
        bag.host = "localhost"
        bag.port = 8000

        assert bag["host"] == "localhost"
        assert bag["port"] == 8000

    def test_set_dict_item(self):
        """Test setting items via dict keys."""
        bag = Bag()
        bag["host"] = "localhost"
        bag["port"] = 8000

        assert bag.host == "localhost"
        assert bag.port == 8000

    def test_del_attribute(self):
        """Test deleting items via attributes."""
        bag = Bag(host="localhost", port=8000)
        del bag.host

        assert "host" not in bag
        assert bag.port == 8000

    def test_attribute_error(self):
        """Test AttributeError for missing keys."""
        bag = Bag(host="localhost")

        with pytest.raises(AttributeError):
            _ = bag.missing_key

    def test_repr(self):
        """Test string representation."""
        bag = Bag(host="localhost", port=8000)
        repr_str = repr(bag)

        assert "Bag(" in repr_str
        assert "host='localhost'" in repr_str
        assert "port=8000" in repr_str

    def test_dict_methods(self):
        """Test that dict methods work."""
        bag = Bag(host="localhost", port=8000)

        assert list(bag.keys()) == ["host", "port"]
        assert list(bag.values()) == ["localhost", 8000]
        assert ("host", "localhost") in bag.items()
