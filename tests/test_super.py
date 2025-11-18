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

    def test_smartsuper_init_skips_class_targets(self):
        """Ensure __init__ is a no-op when decorating classes."""

        class DummyBase:
            pass

        decorator = object.__new__(smartsuper)
        smartsuper.__init__(decorator, DummyBase)

        # __init__ should exit immediately (attributes stay unset)
        assert not hasattr(decorator, "method")
        assert not hasattr(decorator, "owner")

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


class TestSmartSuperAllDecorator:
    """Test @smartsuper.all class decorator."""

    def test_smartsuper_all_skips_manually_marked_methods(self):
        """Methods tagged as BEFORE/AFTER markers should be left untouched."""
        calls = []

        class Base:
            def before(self):
                calls.append("Base.before")

            def after(self):
                calls.append("Base.after")

            def auto(self):
                calls.append("Base.auto")

        def manual_before(self):
            # Simulate manual BEFORE behavior (parent first)
            Base.before(self)
            calls.append("Derived.before")

        manual_before.__smartsuper_mode__ = "before"

        def manual_after(self):
            # Simulate manual AFTER behavior (parent last)
            calls.append("Derived.after")
            Base.after(self)

        manual_after.__smartsuper_mode__ = "after"

        @smartsuper.all
        class Derived(Base):
            before = manual_before
            after = manual_after

            def auto(self):
                calls.append("Derived.auto")

        d = Derived()
        d.before()
        d.after()
        d.auto()

        # manual_before/after must remain untouched, auto should be decorated
        assert Derived.__dict__['before'] is manual_before
        assert Derived.__dict__['after'] is manual_after
        assert isinstance(Derived.__dict__['auto'], smartsuper)

        assert calls == [
            "Base.before", "Derived.before",  # manual BEFORE
            "Derived.after", "Base.after",    # manual AFTER
            "Base.auto", "Derived.auto",      # auto decorated by smartsuper
        ]

    def test_smartsuper_all_decorates_all_overrides(self):
        """Test that @smartsuper.all decorates all overridden methods."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        @smartsuper.all
        class Derived(Base):
            def foo(self):
                calls.append("Derived.foo")

            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        assert calls == ["Base.foo", "Derived.foo", "Base.bar", "Derived.bar"]

    def test_smartsuper_all_respects_explicit_after(self):
        """Test that @smartsuper.all respects explicit @smartsuper.after."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        @smartsuper.all
        class Derived(Base):
            def foo(self):
                calls.append("Derived.foo")

            @smartsuper.after
            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        assert calls == ["Base.foo", "Derived.foo", "Derived.bar", "Base.bar"]

    def test_smartsuper_all_skips_magic_methods(self):
        """Test that @smartsuper.all skips magic methods for safety."""
        calls = []

        class Base:
            def __init__(self):
                calls.append("Base.__init__")

            def normal_method(self):
                calls.append("Base.normal")

        @smartsuper.all
        class Derived(Base):
            def __init__(self):
                calls.append("Derived.__init__")

            def normal_method(self):
                calls.append("Derived.normal")

        d = Derived()
        d.normal_method()

        # __init__ should NOT be auto-decorated, only normal_method should
        assert calls == ["Derived.__init__", "Base.normal", "Derived.normal"]

    def test_smartsuper_all_skips_non_overrides(self):
        """Test that @smartsuper.all only decorates methods that override."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

        @smartsuper.all
        class Derived(Base):
            def foo(self):
                calls.append("Derived.foo")

            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        # foo should be decorated (overrides), bar should not (new method)
        assert calls == ["Base.foo", "Derived.foo", "Derived.bar"]

    def test_smartsuper_all_no_double_decoration(self):
        """Test that @smartsuper.all doesn't double-decorate manual decorations."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        @smartsuper.all
        class Derived(Base):
            @smartsuper
            def foo(self):
                calls.append("Derived.foo")

            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        # Should call each parent exactly once
        assert calls == ["Base.foo", "Derived.foo", "Base.bar", "Derived.bar"]

    def test_smartsuper_all_with_multilevel_inheritance(self):
        """Test @smartsuper.all with multiple inheritance levels."""
        calls = []

        class Base:
            def method(self):
                calls.append("Base")

        class Middle(Base):
            def method(self):
                calls.append("Middle")

        @smartsuper.all
        class Derived(Middle):
            def method(self):
                calls.append("Derived")

        d = Derived()
        d.method()

        # Should call Middle (immediate parent), Middle then calls Base
        assert calls == ["Middle", "Derived"]

    def test_smartsuper_all_skips_properties(self):
        """Test that @smartsuper.all skips properties and attributes."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

        @smartsuper.all
        class Derived(Base):
            value = 42

            def foo(self):
                calls.append("Derived.foo")

        d = Derived()
        d.foo()

        # Should work normally, skipping the 'value' attribute
        assert calls == ["Base.foo", "Derived.foo"]
        assert d.value == 42

    def test_smartsuper_as_class_decorator(self):
        """Test that @smartsuper on a class works like @smartsuper.all."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        @smartsuper
        class Derived(Base):
            def foo(self):
                calls.append("Derived.foo")

            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        # Both methods should be auto-decorated with BEFORE behavior
        assert calls == ["Base.foo", "Derived.foo", "Base.bar", "Derived.bar"]

    def test_smartsuper_class_decorator_with_explicit_after(self):
        """Test that @smartsuper on class respects explicit @smartsuper.after."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

        @smartsuper
        class Derived(Base):
            def foo(self):
                calls.append("Derived.foo")

            @smartsuper.after
            def bar(self):
                calls.append("Derived.bar")

        d = Derived()
        d.foo()
        d.bar()

        # foo should be BEFORE, bar should be AFTER
        assert calls == ["Base.foo", "Derived.foo", "Derived.bar", "Base.bar"]

    def test_smartsuper_all_with_both_explicit_decorators(self):
        """Test that @smartsuper.all handles both @smartsuper and @smartsuper.after."""
        calls = []

        class Base:
            def foo(self):
                calls.append("Base.foo")

            def bar(self):
                calls.append("Base.bar")

            def baz(self):
                calls.append("Base.baz")

        @smartsuper.all
        class Derived(Base):
            @smartsuper
            def foo(self):
                calls.append("Derived.foo")

            @smartsuper.after
            def bar(self):
                calls.append("Derived.bar")

            def baz(self):
                calls.append("Derived.baz")

        d = Derived()
        d.foo()
        d.bar()
        d.baz()

        # foo: already decorated with @smartsuper (BEFORE) - should not double-decorate
        # bar: decorated with @smartsuper.after (AFTER) - should be respected
        # baz: not decorated - should be auto-decorated (BEFORE)
        assert calls == [
            "Base.foo", "Derived.foo",    # foo: BEFORE
            "Derived.bar", "Base.bar",    # bar: AFTER
            "Base.baz", "Derived.baz"     # baz: BEFORE (auto)
        ]
