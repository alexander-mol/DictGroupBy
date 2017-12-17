import time
import math
import numpy as np
from test.test_dict_aggregation import TestDictGroupBy

test_utils = TestDictGroupBy()

data = test_utils.generate_facilities(5)

# goal: calculate the weighted average facility outstanding, weighted by facility outstanding, ignore nans

# 1. using first principle builtins
t0 = time.time()
wavg = 0
w = 0
for i in data:
    if not math.isnan(data[i]['outstanding']) and not math.isnan(data[i]['outstanding']):
        wavg += data[i]['outstanding'] * data[i]['outstanding']
        w += data[i]['outstanding']
wavg /= w
t1 = time.time() - t0
print(t1)

# 2. using list and builtins
t0 = time.time()
values = []
weights = []
for i in data:
    if not math.isnan(data[i]['outstanding']) and not math.isnan(data[i]['outstanding']):
        values.append(data[i]['outstanding'] * data[i]['outstanding'])
        weights.append(data[i]['outstanding'])
wavg = sum(values) / sum(weights)
t1 = time.time() - t0
print(t1)

# 3. using list and numpy
t0 = time.time()
values = []
weights = []
for i in data:
    values.append(data[i]['outstanding'] * data[i]['outstanding'])
    weights.append(data[i]['outstanding'])
wavg = np.nansum(values) / np.nansum(weights)
t1 = time.time() - t0
print(t1)

# 4. using numpy frame
t0 = time.time()
values = []
weights = []
for i in data:
    values.append(data[i]['outstanding'] * data[i]['outstanding'])
    weights.append(data[i]['outstanding'])
values = np.array(values)
weights = np.array(weights)
wavg = np.nansum(values) / np.nansum(weights)
t1 = time.time() - t0
print(t1)