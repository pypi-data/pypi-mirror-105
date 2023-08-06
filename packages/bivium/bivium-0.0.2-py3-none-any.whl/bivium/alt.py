"""Alternative mutable version of Bivium, which behaves more like a dict.
It implements all container type methods, and some of them also in the reverse direction.
This version doesn't need to be subclassed and can be instantiated by itself:

t = Bivium({"A": 1, "B": 2}, C=3)

Notice that you can use both a mapping or kwargs to instantiate the Bivium.
Note that a KeyError will be raised if you try to pass the same key in the mapping and kwargs.

Also, if any keys in the mapping or kwargs have the same value, the init will raise a ValueError.
Similalry, ValueErrors will be raised later if you try to add a value under some key which
already is the value for some other key.

_default_key_ and _default_value_ still exist, but you should probably use .get() and .rget() methods instead.
"""

from typing import Any
from itertools import chain


__all__ = ["Bivium"]


class _empty:

    @staticmethod
    def items():
        return {}


class Bivium:

    def __init__(self, content: dict = _empty, **kwargs: Any):
        self.__key2value_map = {}
        self.__value2key_map = {}
        self._default_key_: Any = _empty
        self._default_value_: Any = _empty
        self.update(content, **kwargs)

    def __getitem__(self, key):
        try:
            return self.__key2value_map[key]
        except KeyError as e:
            if self._default_key_ is not _empty:
                return self._default_key_
            raise e

    def __setitem__(self, key, value):
        if value in self.__value2key_map:
            raise ValueError(f"'{self.__value2key_map[value]}' already has the value '{value}'")

        if key in self.__key2value_map:
            del self.__value2key_map[self.__key2value_map[key]]

        self.__key2value_map[key] = value
        self.__value2key_map[value] = key

    def __delitem__(self, key):
        del self.__value2key_map[self.__key2value_map[key]]
        del self.__key2value_map[key]

    def __call__(self, value):
        try:
            return self.__value2key_map[value]
        except KeyError as e:
            if self._default_value_ is not _empty:
                return self._default_value_
            raise e

    def __contains__(self, key):
        return key in self.__key2value_map or key in self.__value2key_map

    def __len__(self):
        return len(self.__key2value_map)

    def __iter__(self):
        return iter(self.__key2value_map)

    def __reversed__(self):
        return reversed(self.__key2value_map)

    def __str__(self):
        return "{" + ", ".join([f"{key}={value}" for key, value in self.__key2value_map.items()]) + "}"

    def get(self, key, default: Any = None):
        return self.__key2value_map.get(key, default)

    def rget(self, value, default: Any = None):
        return self.__value2key_map.get(value, default)

    def setdefault(self, key, default: Any = None):
        if default in self.__value2key_map:
            raise ValueError(f"'{self.__value2key_map[default]}' already has the value '{default}'")

        old_value = self.__key2value_map.get(key, _empty)
        value = self.__key2value_map.setdefault(key, default)
        if value == default:
            if old_value != _empty:
                del self.__value2key_map[old_value]
            self.__value2key_map[value] = key

        return value

    def rsetdefault(self, value, default: Any = None):
        if default in self.__key2value_map:
            raise ValueError(f"'{self.__key2value_map[default]}' is already the value for '{default}'")

        old_key = self.__value2key_map.get(value, _empty)
        key = self.__value2key_map.setdefault(value, default)
        if key == default:
            if old_key != _empty:
                del self.__key2value_map[key]
            self.__key2value_map[key] = value

        return key

    def keys(self):
        return self.__key2value_map.keys()

    def values(self):
        return self.__key2value_map.values()

    def clear(self):
        self.__key2value_map.clear()
        self.__value2key_map.clear()

    def pop(self, key, default: Any = _empty):
        if default == _empty:
            value = self.__key2value_map.pop(key)
        else:
            value = self.__key2value_map.pop(key, default)

        if value == default:
            del self.__value2key_map[value]

        return value

    def rpop(self, value, default: Any = _empty):
        if default == _empty:
            key = self.__value2key_map.pop(value)
        else:
            key = self.__value2key_map.pop(value, default)

        if key == default:
            del self.__key2value_map[key]

        return key

    def popitem(self):
        key, value = self.__key2value_map.popitem()
        del self.__value2key_map[value]
        return key, value

    def copy(self):
        new = self.__class__(self.__key2value_map)
        new._default_key_ = self._default_key_
        new._default_value_ = self._default_value_
        return new

    def update(self, content: dict = _empty, **kwargs: Any):
        for key, value in content.items():
            if key in kwargs:
                raise KeyError(f"'{key}' can't be defined in both 'content' and 'kwargs'.")

        to_update = {key: value for key, value in chain(content.items(), kwargs.items())}

        if len(set(to_update.values())) < len(to_update):
            raise ValueError(f"Trying to update the same value to multiple keys. Aborting.")

        non_updated_values = [value for key, value in self.__key2value_map.items() 
                              if to_update.get(key, _empty) == _empty]

        for key, value in to_update.items():
            if value in non_updated_values:
                raise ValueError(f"'{self.__value2key_map[value]}' and '{key}' would have "
                                 f"the same value '{value}'. Aborting.")

        for key, value in to_update.items():
            self.__key2value_map.pop(key, None)
            self.__value2key_map.pop(value, None)
        
        for key, value in to_update.items():
            self.__key2value_map[key] = value
            self.__value2key_map[value] = key
