"""Tests for the smartsuper decorator."""

import pytest
from smartseeds import smartsuper


class TestSmartSuperDecorator:
    """Test @smartsuper decorator (call parent before)."""

    def test_smartsuper_calls_parent_before(self):
        """Test that @smartsuper calls parent method before current method."""
        calls = []

        class Base:
            def method(self):
                calls.append("Base")

        class Derived(Base):
            @smartsuper
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        assert calls == ["Base", "Derived"]

    def test_smartsuper_works_with_init(self):
        """Test that @smartsuper works with __init__."""
        calls = []

        class Base:
            def __init__(self):
                calls.append("Base.__init__")

        class Derived(Base):
            @smartsuper
            def __init__(self):
                calls.append("Derived.__init__")

        Derived()

        assert calls == ["Base.__init__", "Derived.__init__"]

    def test_smartsuper_with_arguments(self):
        """Test that @smartsuper forwards arguments correctly."""
        results = []

        class Base:
            def method(self, x, y=10):
                results.append(("Base", x, y))

        class Derived(Base):
            @smartsuper
            def method(self, x, y=10):
                results.append(("Derived", x, y))

        d = Derived()
        d.method(5, y=20)

        assert results == [("Base", 5, 20), ("Derived", 5, 20)]

    def test_smartsuper_with_no_parent_method(self):
        """Test that @smartsuper doesn't fail if parent method doesn't exist."""
        calls = []

        class Base:
            pass

        class Derived(Base):
            @smartsuper
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        assert calls == ["Derived"]

    def test_smartsuper_with_return_value(self):
        """Test that @smartsuper returns the decorated method's return value."""

        class Base:
            def method(self):
                return "Base"

        class Derived(Base):
            @smartsuper
            def method(self):
                return "Derived"

        d = Derived()
        result = d.method()

        assert result == "Derived"

    def test_smartsuper_multilevel_inheritance(self):
        """Test @smartsuper with multiple inheritance levels."""
        calls = []

        class Base:
            def method(self):
                calls.append("Base")

        class Middle(Base):
            @smartsuper
            def method(self):
                calls.append("Middle")

        class Derived(Middle):
            @smartsuper
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        assert calls == ["Base", "Middle", "Derived"]


class TestSmartSuperAfterDecorator:
    """Test @smartsuper.after decorator (call parent after)."""

    def test_smartsuper_after_calls_parent_after(self):
        """Test that @smartsuper.after calls parent method after current method."""
        calls = []

        class Base:
            def method(self):
                calls.append("Base")

        class Derived(Base):
            @smartsuper.after
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        assert calls == ["Derived", "Base"]

    def test_smartsuper_after_with_init(self):
        """Test that @smartsuper.after works with __init__."""
        calls = []

        class Base:
            def __init__(self):
                calls.append("Base.__init__")

        class Derived(Base):
            @smartsuper.after
            def __init__(self):
                calls.append("Derived.__init__")

        Derived()

        assert calls == ["Derived.__init__", "Base.__init__"]

    def test_smartsuper_after_with_arguments(self):
        """Test that @smartsuper.after forwards arguments correctly."""
        results = []

        class Base:
            def method(self, x, y=10):
                results.append(("Base", x, y))

        class Derived(Base):
            @smartsuper.after
            def method(self, x, y=10):
                results.append(("Derived", x, y))

        d = Derived()
        d.method(5, y=20)

        assert results == [("Derived", 5, 20), ("Base", 5, 20)]

    def test_smartsuper_after_with_no_parent_method(self):
        """Test that @smartsuper.after doesn't fail if parent method doesn't exist."""
        calls = []

        class Base:
            pass

        class Derived(Base):
            @smartsuper.after
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        assert calls == ["Derived"]

    def test_smartsuper_after_with_return_value(self):
        """Test that @smartsuper.after returns the decorated method's return value."""

        class Base:
            def method(self):
                return "Base"

        class Derived(Base):
            @smartsuper.after
            def method(self):
                return "Derived"

        d = Derived()
        result = d.method()

        assert result == "Derived"


class TestSmartSuperEdgeCases:
    """Test edge cases and special scenarios."""

    def test_smartsuper_with_mixed_decorators(self):
        """Test using both @smartsuper and @smartsuper.after in same class."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        class Derived(Base):
            @smartsuper
            def foo(self):
                calls.append("Derived.foo")

            @smartsuper.after
            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        assert calls == ["Base.foo", "Derived.foo", "Derived.bar", "Base.bar"]

    def test_smartsuper_preserves_method_name(self):
        """Test that decorator preserves method name."""

        class Base:
            def method(self):
                pass

        class Derived(Base):
            @smartsuper
            def method(self):
                pass

        assert Derived.method.name == "method"

    def test_smartsuper_with_property_like_access(self):
        """Test accessing decorated method as class attribute."""

        class Base:
            def method(self):
                return "Base"

        class Derived(Base):
            @smartsuper
            def method(self):
                return "Derived"

        # Accessing on class returns the descriptor
        assert isinstance(Derived.method, smartsuper)

        # Accessing on instance returns the wrapper
        d = Derived()
        assert callable(d.method)
