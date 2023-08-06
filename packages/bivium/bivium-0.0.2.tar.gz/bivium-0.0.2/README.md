# Bivium - Two-way Enum-like lookups

Bivium is a enum-like immutable object you can inherit from to define two-way lookups.
Create a class like this:
```python
class Test(Bivium):
    A = 1
    B = 2
    C = 3
```
Then, you can do lookups on the data like this:
```python
Test.A     # 1
Test["A"]  # 1
Test(1)    # A
```
Bivium does not recognize dunder or sunder methods (i.e. \_\_abc\_\_ or \_abc\_)
or anything that looks like it, so this will not work:
```python
class Test(Bivium):
    _A_ = 1    # nope
    __A__ = 1  # double nope
```
You can set the optional `_default_key_` and `_default_value_` attributes, which will be returned
if no keys or values are found when using `Test[key]` or `Test(value)` respectively.
```python
class Test(Bivium):
    A = 1
    B = 2
    C = 3
    
    _default_key_ = "foo"
    _default_value_ = "bar"
    
Test["X"]  # "foo"
Test("Y")  # "bar"
```
If they are not set, ValueErrors are raised for missing data.
Attribute access (e.g. `Test.A`) will always raise an error for missing data.

---

There is also and alternative mutable version of Bivium, which behaves more like a dict.
It implements all container type methods, and some of them also in the reverse direction.

This version should be instantiated:
```python
test = Bivium({"A": 1, "B": 2}, C=3)
```
Notice that you can use both a mapping or kwargs to instantiate the Bivium.
Note that a KeyError will be raised if you try to pass the same key in the mapping and kwargs.

Also, if any keys in the mapping or kwargs have the same value, the init will raise a ValueError.
Similalry, ValueErrors will be raised later if you try to add a value under some key which already is the value for some other key.

Bivium alt still has `_default_key_` and `_default_value_`, but you should probably use `.get()` and `.rget()` methods instead.
