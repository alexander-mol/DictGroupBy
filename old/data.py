import random

def get_data(n=100, m=20):
    out = {}
    for i in range(n):
        out[i] = dict((j, gen_type(j)) for j in range(m))
    return out

def gen_type(j):
    if j % 3 == 0:
        return f'{chr(random.randint(65,123))}'
    if j % 3 == 1:
        return random.randint(-100, 100)
    else:
        return (random.random() - 0.5) * 200
