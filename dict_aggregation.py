import copy
import aggregation_utils as au


class DictAggregation:

    def __init__(self, dict):
        self.dict = dict

    def aggregate(self, dict, instructions):
        group_keys = self.get_top_level_group_keys(instructions)
        grouped_dict = {}
        for i in dict:
            group_value = self.make_group_key(dict[i], group_keys)
            try:
                grouped_dict[group_value].update({i: dict[i]})
            except KeyError:
                grouped_dict[group_value] = {i: dict[i]}
        # so now we have grouped all records by their top level group keys
        # what still needs to be done is now to aggregate each group into a single record (and append all sub records)
        # and then to repeat the process on the sub records
        this_level_instructions = self.get_instructions_this_level(instructions)
        level_portals = self.get_sub_level_portals(this_level_instructions)
        aggregated_dict = {}
        for group_key, group in grouped_dict.items():
            group_rep = next(iter(group.values()))
            # aggregation of this group, current level
            for instruction in this_level_instructions:
                if isinstance(instruction, tuple):
                    try:
                        group_rep[instruction[0]] = instruction[1](group, instruction[0])
                    except TypeError:
                        group_rep[instruction[0]] = instruction[1][0](group, instruction[0], instruction[1][1])
                else:
                    # then this is a level portal, and we append the sub records to the existing group sub records
                    key = next(iter(instruction.keys()))
                    group_rep[key].update(au.collect(group, key))
            # use recursion here to join sub-records
            for level_portal in level_portals:
                level_portal_key = next(iter(level_portal.keys()))  # e.g. 'transactions'
                group_rep[level_portal_key] = self.aggregate(group_rep[level_portal_key],
                                                             level_portal[level_portal_key])
            aggregated_dict[group_key] = group_rep
        return aggregated_dict

    def get_top_level_group_keys(self, instructions):
        return [item for item in instructions if len(item) == 1 and isinstance(item, tuple)]

    def get_instructions_this_level(self, instructions):
        return [item for item in instructions if not (len(item) == 1 and isinstance(item, tuple))]

    def get_sub_level_portals(self, instructions):
        return [item for item in instructions if isinstance(item, dict)]

    @staticmethod
    def concat(values):
        return '|'.join(values)

    def make_group_key(self, record, group_keys):
        keys = []
        for feature in group_keys:
            keys.append(record[feature[0]])
        return self.concat(keys)



if __name__ == '__main__':
    data = {0: {'facility_type': 'b', 'outstanding': 70,
                'transactions': {0: {'transaction_type': 'b', 'outstanding': 5},
                                 1: {'transaction_type': 'b', 'outstanding': 65}}},
            1: {'facility_type': 'a', 'outstanding': 135,
                'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                 3: {'transaction_type': 'b', 'outstanding': 74}}},
            2: {'facility_type': 'b', 'outstanding': 211,
                'transactions': {4: {'transaction_type': 'a', 'outstanding': 36},
                                 5: {'transaction_type': 'a', 'outstanding': 96},
                                 6: {'transaction_type': 'a', 'outstanding': 79}}},
            3: {'facility_type': 'a', 'outstanding': 209,
                'transactions': {7: {'transaction_type': 'c', 'outstanding': 77},
                                 8: {'transaction_type': 'a', 'outstanding': 39},
                                 9: {'transaction_type': 'a', 'outstanding': 93}}}}

    instructions = [('facility_type',), ('outstanding', au.sum), {'transactions': [('transaction_type',),
                                                                                 ('outstanding', au.sum)]}]
    print(DictAggregation(data).aggregate(data, instructions))
    print(data)
