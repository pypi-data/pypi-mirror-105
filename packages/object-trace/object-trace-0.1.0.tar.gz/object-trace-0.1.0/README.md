Trace every use of selected objects.

# Example
Running `python example.py` prints the following:
```
# Trace for label=`a`
_   : call `<module>` (example.py:1)    | 
  26  : call `func` (example.py:11)       | func()
    13  : use                               | trace(a, label="a")
    13  : RC 2->5                           | trace(a, label="a")
    15  : use                               | data["b"] = f2(a)
    15  : call `f2` (example.py:7)          | data["b"] = f2(a)
      7   : RC 5->6                           | def f2(x):
      8   : use                               | return x
    15  : use                               | data["b"] = f2(a)
    16  : RC 6->5                           | a = 11
    17  : RC 5->4                           | data["b"] = f2(3)
--------------------------------------------------------------------------------
# Trace for label=`3`
_   : call `<module>` (example.py:1)    | 
  26  : call `func` (example.py:11)       | func()
    14  : use                               | data["a"] = trace(3, label="3")
    14  : RC 32->34                         | data["a"] = trace(3, label="3")
    15  : RC 34->35                         | data["b"] = f2(a)
    17  : use                               | data["b"] = f2(3)
    17  : call `f2` (example.py:7)          | data["b"] = f2(3)
      8   : use                               | return x
    17  : use                               | data["b"] = f2(3)
    18  : use                               | data["a"] = trace(3, label="3")
    18  : use                               | data["a"] = trace(3, label="3")
    19  : RC 36->38                         | 2 + 4
    20  : use                               | str(3) + str(3 + 1)
    22  : use                               | data["c"] = data["a"]
  27  : use                               | x = data["b"]
  27  : RC 38->39                         | x = data["b"]
  28  : use                               | x = x + x
  28  : use                               | x = x + x
--------------------------------------------------------------------------------
# Trace for label=`3`
_   : call `<module>` (example.py:1)    | 
  26  : call `func` (example.py:11)       | func()
    18  : use                               | data["a"] = trace(3, label="3")
    19  : RC 36->38                         | 2 + 4
    20  : use                               | str(3) + str(3 + 1)
    22  : use                               | data["c"] = data["a"]
  27  : use                               | x = data["b"]
  27  : RC 38->39                         | x = data["b"]
  28  : use                               | x = x + x
  28  : use                               | x = x + x
--------------------------------------------------------------------------------
```
