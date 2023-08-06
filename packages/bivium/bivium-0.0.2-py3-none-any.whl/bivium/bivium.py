"""Bivium is a enum-like immutable object you can inherit from to define two-way lookups.

Create a class like this:

class Test(Bivium):
    A = 1
    B = 2
    C = 3

Then, you can do lookups on the data like this:

Test.A     # 1
Test["A"]  # 1
Test(1)    # A

Bivium does not recognize dunder or sunder methods (i.e. __abc__ or _abc_)
or anything that looks like it, so this will not work:

class Test(Bivium):
    _A_ = 1    # nope
    __A__ = 1  # double nope

You can set the optional '_default_key_' and '_default_value_' attributes, which will be returned
if no keys or values are found when using Test[key] or Test(value) respectively.

class Test(Bivium):
    A = 1
    B = 2
    C = 3
    
    _default_key_ = "foo"
    _default_value_ = "bar"
    
Test["X"]  # "foo"
Test("Y")  # "bar"

If they are not set, ValueErrors are raised for missing data.
Attribute access (e.g. Test.A) will always raise an error for missing data.
"""

from typing import Any


__all__ = ["Bivium"]


class _empty:
    pass


def _is_dunder(name):
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_'


def _is_sunder(name):
    return len(name) > 2 and name[0] == name[-1] == '_' and name[1:2] != '_' and name[-2:-1] != '_'


class _BiviumMeta(type):

    _default_key_ = _empty
    _default_value_ = _empty

    def __new__(mcs, cls, bases, classdict):
        _new_class_ = super().__new__(mcs, cls, bases, classdict)
        _new_class_._key2value_map_: dict = _empty  # noqa
        _new_class_._value2key_map_: dict = _empty  # noqa

        for key, value in classdict.items():
            if _is_sunder(key) or _is_dunder(key):
                continue

            if value in _new_class_._value2key_map_:
                raise ValueError(f"'{_new_class_._value2key_map_[value]}' and '{key}' have the same value '{value}'")

            _new_class_._key2value_map_[key] = value
            _new_class_._value2key_map_[value] = key

        return _new_class_
    
    def __setattr__(cls, key, value):
        if key in ["_key2value_map_", "_value2key_map_"] and value == _empty:
            super().__setattr__(key, {})
        else:
            raise AttributeError("Bivium is immutable.")

    def __delattr__(cls, key):
        raise AttributeError("Bivium is immutable.")

    def __getitem__(cls, key):
        try:
            return cls._key2value_map_[key]
        except KeyError as e:
            if cls._default_key_ is not _empty:
                return cls._default_key_
            raise e

    def __call__(cls, value: Any = _empty):
        if value == _empty:
            raise TypeError("Bivium should not be instantiated.")

        try:
            return cls._value2key_map_[value]
        except KeyError as e:
            if cls._default_value_ is not _empty:
                return cls._default_value_
            raise e

    def __bool__(self):
        return True

    def __str__(cls):
        return "{" + ", ".join([f"{key}={value}" for key, value in cls._key2value_map_.items()]) + "}"


class Bivium(metaclass=_BiviumMeta):
    pass
