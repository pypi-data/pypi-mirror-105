# Modify Range of numbers

Modify the range of collection of numbers on scale of log5 for better visualization. It works best between 0-100. max,min are the max and min value from the present list and, a and b are the max and min values you want of the new range. It is then converted into logarithmic scale.

Run the following to install:
```python
pip install modify_range
```
---

### Is based on the formula:
    f(x) = (b-a)(x-min)/(max-min)      
---

To convert:
```python
from modify_range import change_range
...
...
x = change_range(x,min,max,a,b)
```
Here,
- x   = integer from the list
- min = min value from the list
- max = max value from the list
- a   = new maximum value</li>
- b   = new minimum value</li>

To get back the values: __(not recommended to use, as original values are lost while converting to logarithmic scale. Exact values cannot be obtained)__
```python
x = inverse_range(x,min,max,a,b)
```
Here,
- x = integer value from the modified list
- max = maximum integer value from the modified list
- min = minimum integer value from the modified list
- a   = max value from the original list
- b   = min value from the original list
