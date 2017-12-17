import copy

class DictGroupBy:

    def __init__(self, dict, group_features):
        self.group_features = group_features
        self.groupby_obj = {}
        for i in dict:
            group_key = self.make_group_key(dict[i], group_features)
            if group_key in self.groupby_obj:
                self.groupby_obj[group_key].update({i: dict[i]})
            else:
                self.groupby_obj[group_key] = {i: dict[i]}

    def __str__(self):
        return self.groupby_obj.__str__()

    def __getitem__(self, columns):
        output = {}
        for group in self.groupby_obj:
            for i in self.groupby_obj[group]:
                try:
                    output[group].update(
                        {i: copy.deepcopy(dict((col, self.groupby_obj[group][i][col]) for col in columns))})
                except KeyError:
                    output[group] = {i: copy.deepcopy(dict((col, self.groupby_obj[group][i][col]) for col in columns))}
        return output

    @staticmethod
    def keyfunc(values):
        return '|'.join(values)

    def make_group_key(self, row, group_features, use_hierarchy):
        keys = []
        for feature in group_features:
            keys.append(row[feature])
        return self.keyfunc(keys)

    def sum(self):
        output_dict = {}
        for group in self.groupby_obj:
            column_total = {}
            for i in self.groupby_obj[group]:
                for col in self.groupby_obj[group][i]:
                    if col in self.group_features:
                        continue
                    try:
                        column_total[col] += self.groupby_obj[group][i][col]
                    except KeyError:
                        column_total[col] = self.groupby_obj[group][i][col]
            output_dict[group] = column_total
        return output_dict

    def max(self):
        output_dict = {}
        for group in self.groupby_obj:
            column_max = {}
            for i in self.groupby_obj[group]:
                for col in self.groupby_obj[group][i]:
                    if col in self.group_features:
                        continue
                    try:
                        if column_max[col] < self.groupby_obj[group][i][col]:
                            column_max[col] = self.groupby_obj[group][i][col]
                    except KeyError:
                        column_max[col] = self.groupby_obj[group][i][col]
            output_dict[group] = column_max
        return output_dict

    def min(self):
        output_dict = {}
        for group in self.groupby_obj:
            column_min = {}
            for i in self.groupby_obj[group]:
                for col in self.groupby_obj[group][i]:
                    try:
                        if column_min[col] > self.groupby_obj[group][i][col]:
                            column_min[col] = self.groupby_obj[group][i][col]
                    except KeyError:
                        column_min[col] = self.groupby_obj[group][i][col]
            output_dict[group] = column_min
        return output_dict

    def count(self):
        output_dict = {}
        for group in self.groupby_obj:
            column_count = {}
            for i in self.groupby_obj[group]:
                for col in self.groupby_obj[group][i]:
                    try:
                        column_count[col] += 1
                    except KeyError:
                        column_count[col] = 1
            output_dict[group] = column_count
        return output_dict

    # def realize(self, sum_columns=None, avg_columns=None, max_columns=None, min_columns=None, count_columns=None):

    # @staticmethod
    # def merge(dicts):
    #     for group in dicts[0]:

if __name__ == '__main__':
    # data_set1 = {0: {'type': 'a', 'value': 3}, 1: {'type': 'b', 'value': 2}, 2: {'type': 'a', 'value': 1}}
    # data_set2 = {0: {'type1': 'a', 'type2': 'a', 'value': 3}, 1: {'type1': 'b', 'type2': 'a', 'value': 2}, 2: {'type1': 'a', 'type2': 'a', 'value': 1}}
    # gb_obj = DictGroupByObj(data_set2, ['type1', 'type2'])
    # print(gb_obj)
    # print(gb_obj[['type1', 'value']])
    # print(gb_obj[['type2', 'value']])
    # print(gb_obj.sum())
    data = {0: {'facility_type': 'b', 'outstanding': 70,
                'transactions': {0: {'transaction_type': 'b', 'outstanding': 5},
                                 1: {'transaction_type': 'b', 'outstanding': 65}}},
            1: {'facility_type': 'a', 'outstanding': 135,
                'transactions': {0: {'transaction_type': 'b', 'outstanding': 61},
                                 1: {'transaction_type': 'b', 'outstanding': 74}}},
            2: {'facility_type': 'b', 'outstanding': 211,
                'transactions': {0: {'transaction_type': 'a', 'outstanding': 36},
                                 1: {'transaction_type': 'a', 'outstanding': 96},
                                 2: {'transaction_type': 'a', 'outstanding': 79}}},
            3: {'facility_type': 'a', 'outstanding': 209,
                'transactions': {0: {'transaction_type': 'c', 'outstanding': 77},
                                 1: {'transaction_type': 'a', 'outstanding': 39},
                                 2: {'transaction_type': 'a', 'outstanding': 93}}}}

    group_features = ['facility_type', {'transactions': ['transaction_type']}]
    print(DictGroupBy(data, group_features).sum())
