import groupby
import random
import time
import pandas as pd

def generate_record():
    return {
        'gcol1': random.choice(['a', 'b', 'c']), 'gcol2': random.choice(['a', 'b', 'c']),
        'gcol3': random.choice(['a', 'b', 'c']), 'vcol1': random.randint(0, 100), 'vcol2': random.random(),
        'vcol3': random.randint(0, 2)
    }

data = {}
for i in range(100000):
    data[i] = generate_record()
print('Generated data.')
group_columns = ['gcol1', 'gcol2', 'gcol3']

t0 = time.time()
gb = groupby.GroupByObj(data, group_columns)
t1 = time.time()
out = gb.sum()
tf = time.time()
# print(out)
print(t1 - t0, tf - t1, tf - t0)

# df = pd.DataFrame(data).T
# t0 = time.time()
# df.groupby(group_columns).sum()
# tf = time.time()
# # print(out)
# print(tf - t0)