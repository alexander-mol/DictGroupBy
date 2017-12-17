import math

def sum(dict, field):
    total = 0.
    for record in dict.values():
        if not math.isnan(record[field]):
            total += record[field]
    return total

def min(dict, field):
    min_value = math.inf
    for record in dict.values():
        if not math.isnan(record[field]) and min_value > record[field]:
            min_value = record[field]
    return min_value

def max(dict, field):
    max_value = -math.inf
    for record in dict.values():
        if not math.isnan(record[field]) and max_value < record[field]:
            max_value = record[field]
    return max_value

def count(dict, field):
    total = 0
    for record in dict.values():
        if not math.isnan(record[field]):
            total += 1
    return total

def average(dict, field):
    total = 0.
    count = 0
    for record in dict.values():
        if not math.isnan(record[field]):
            total += record[field]
            count += 1
    return total / count

def weighted_average(dict, field, weight_field):
    total = 0.
    weight = 0
    for record in dict.values():
        if not math.isnan(record[field]) and not math.isnan(record[weight_field]):
            total += record[field]
            weight += record[weight_field]
    return total / weight

def arg_min(dict, field, min_field):
    max_value = math.inf
    arg_value = None
    for record in dict.values():
        if not math.isnan(record[min_field]) and not math.isnan(record[field]) and max_value > record[min_field]:
            max_value = record[min_field]
            arg_value = record[field]
    return arg_value

def arg_max(dict, field, max_field):
    max_value = -math.inf
    arg_value = None
    for record in dict.values():
        if not math.isnan(record[max_field]) and not math.isnan(record[field]) and max_value < record[max_field]:
            max_value = record[max_field]
            arg_value = record[field]
    return arg_value

def collect(dict, field):
    out = {}
    for record in dict.values():
        out.update(record[field])
    return out
