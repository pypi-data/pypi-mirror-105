#Modify Range of numbers

Modify the range of collection of numbers on scale of log5 for better visualization. It works best between 0-100. max,min is the max and min value from the present list and, a and b are the max and min values you want. It will set values between a and b. Then convert it to the scale of log5.

Run the following to install:

```python
pip install modify_range

'''Is based on the simple formula: 
    f(x) = (b-a)(x-min)/(max-min)'''
```
To use:
```python
from modify_range import change_range
...
...
x = change_range(x,min,max,a,b)
```
Here, x   = integer from the list
      min = min value from the list
      max = max value from the list
      a   = new maximum value
      b   = new minimum value
