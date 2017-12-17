import unittest
import time
import random
from dict_aggregation import DictAggregation
import aggregation_utils as au

class TestDictGroupBy(unittest.TestCase):

    def generate_transaction(self):
        return {
            'transaction_type': random.choice('abcedefghijklmn'),
            'outstanding': random.randint(0, 100)
        }

    def generate_facility(self):
        num_transactions = random.randint(1, 10)
        transactions = {}
        outstanding = 0
        for i in range(num_transactions):
            transactions[i] = self.generate_transaction()
            outstanding += transactions[i]['outstanding']

        return {
            'facility_type': random.choice('abcdefghijklmn'),
            'outstanding': outstanding,
            'transactions': transactions
        }

    def generate_facilities(self, num):
        out = {}
        for i in range(num):
            out[i] = self.generate_facility()
        return out

    def test_speed(self):
        data = self.generate_facilities(1000)
        t0 = time.time()
        instructions = [('facility_type',), ('outstanding', au.sum), {'transactions': [('transaction_type',),
                                                                                      ('outstanding', au.sum)]}]
        output = DictAggregation(data).aggregate(data, instructions)
        print(time.time() - t0, 'should be roughly 0.006 s')

    def test_end_to_end(self):
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

        expected_output = {'b': {'facility_type': 'b', 'outstanding': 281,
                                 'transactions': {'a': {'transaction_type': 'a', 'outstanding': 211},
                                                  'b': {'transaction_type': 'b', 'outstanding': 70}}},
                           'a': {'facility_type': 'a', 'outstanding': 344,
                                 'transactions': {'c': {'transaction_type': 'c', 'outstanding': 77},
                                                  'a': {'transaction_type': 'a', 'outstanding': 132},
                                                  'b': {'transaction_type': 'b', 'outstanding': 135}}}}

        instructions = [('facility_type',), ('outstanding', au.sum), {'transactions': [('transaction_type',),
                                                                                      ('outstanding', au.sum)]}]
        output = DictAggregation(data).aggregate(data, instructions)

        assert output == expected_output

    def test_end_to_end_3_levels(self):
        data = {0: {'facility_type': 'b', 'outstanding': 70,
                    'transactions': {0: {'transaction_type': 'b', 'outstanding': 5,
                                         'transaction_collaterals': {0: {'type': 'a', 'value': 28}}},
                                     1: {'transaction_type': 'b', 'outstanding': 65,
                                         'transaction_collaterals': {1: {'type': 'b', 'value': 21}}}}},
                1: {'facility_type': 'a', 'outstanding': 135,
                    'transactions': {2: {'transaction_type': 'a', 'outstanding': 61,
                                         'transaction_collaterals': {2: {'type': 'a', 'value': 34}}},
                                     3: {'transaction_type': 'b', 'outstanding': 74,
                                         'transaction_collaterals': {3: {'type': 'b', 'value': 46}}}}},
                2: {'facility_type': 'b', 'outstanding': 211,
                    'transactions': {4: {'transaction_type': 'b', 'outstanding': 36,
                                         'transaction_collaterals': {4: {'type': 'a', 'value': 57}}},
                                     5: {'transaction_type': 'a', 'outstanding': 96,
                                         'transaction_collaterals': {5: {'type': 'a', 'value': 62}}},
                                     6: {'transaction_type': 'a', 'outstanding': 79,
                                         'transaction_collaterals': {6: {'type': 'b', 'value': 71}}}}},
                3: {'facility_type': 'a', 'outstanding': 209,
                    'transactions': {7: {'transaction_type': 'c', 'outstanding': 77,
                                         'transaction_collaterals': {7: {'type': 'a', 'value': 79}}},
                                     8: {'transaction_type': 'a', 'outstanding': 39,
                                         'transaction_collaterals': {8: {'type': 'a', 'value': 83}}},
                                     9: {'transaction_type': 'a', 'outstanding': 93,
                                         'transaction_collaterals': {9: {'type': 'b', 'value': 92}}}}}}

        expected_output = {'b': {'facility_type': 'b', 'outstanding': 281,
                                 'transactions': {
                                     'b': {'transaction_type': 'b', 'outstanding': 106,
                                           'transaction_collaterals': {'b': {'type': 'b', 'value': 21},
                                                                       'a': {'type': 'a', 'value': 85}}},
                                     'a': {'transaction_type': 'a', 'outstanding': 175,
                                           'transaction_collaterals': {'b': {'type': 'b', 'value': 71},
                                                                       'a': {'type': 'a', 'value': 62}}}
                                 }},
                           'a': {'facility_type': 'a', 'outstanding': 344,
                                 'transactions': {
                                     'c': {'transaction_type': 'c', 'outstanding': 77,
                                           'transaction_collaterals': {'a': {'type': 'a', 'value': 79}}},
                                     'a': {'transaction_type': 'a', 'outstanding': 193,
                                           'transaction_collaterals': {'a': {'type': 'a', 'value': 117},
                                                                       'b': {'type': 'b', 'value': 92}}},
                                     'b': {'transaction_type': 'b', 'outstanding': 74,
                                           'transaction_collaterals': {'b': {'type': 'b', 'value': 46}}}}}}

        instructions = [('facility_type',), ('outstanding', au.sum),
                        {'transactions': [('transaction_type',), ('outstanding', au.sum),
                                          {'transaction_collaterals': [('type',), ('value', au.sum)]}]}]

        output = DictAggregation(data).aggregate(data, instructions)
        assert output == expected_output

    def test_end_to_end_multiple_group_fields(self):
        data = {0: {'facility_type': 'b', 'customer_type': 'M', 'outstanding': 70,
                    'transactions': {0: {'transaction_type': 'b', 'outstanding': 5},
                                     1: {'transaction_type': 'b', 'outstanding': 65}}},
                1: {'facility_type': 'a', 'customer_type': 'M', 'outstanding': 135,
                    'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                     3: {'transaction_type': 'b', 'outstanding': 74}}},
                2: {'facility_type': 'b', 'customer_type': 'M', 'outstanding': 211,
                    'transactions': {4: {'transaction_type': 'a', 'outstanding': 36},
                                     5: {'transaction_type': 'a', 'outstanding': 96},
                                     6: {'transaction_type': 'a', 'outstanding': 79}}},
                3: {'facility_type': 'a', 'customer_type': 'F', 'outstanding': 209,
                    'transactions': {7: {'transaction_type': 'c', 'outstanding': 77},
                                     8: {'transaction_type': 'a', 'outstanding': 39},
                                     9: {'transaction_type': 'a', 'outstanding': 93}}}}

        expected_output = {'b|M': {'facility_type': 'b', 'customer_type': 'M', 'outstanding': 281,
                                   'transactions': {'a': {'transaction_type': 'a', 'outstanding': 211},
                                                    'b': {'transaction_type': 'b', 'outstanding': 70}}},
                           'a|M': {'facility_type': 'a', 'customer_type': 'M', 'outstanding': 135,
                                   'transactions': {'b': {'transaction_type': 'b', 'outstanding': 135}}},
                           'a|F': {'facility_type': 'a', 'customer_type': 'F', 'outstanding': 209,
                                   'transactions': {'c': {'transaction_type': 'c', 'outstanding': 77},
                                                    'a': {'transaction_type': 'a', 'outstanding': 132}}}}

        instructions = [('facility_type',), ('customer_type',), ('outstanding', au.sum),
                        {'transactions': [('transaction_type',), ('outstanding', au.sum)]}]
        output = DictAggregation(data).aggregate(data, instructions)
        assert output == expected_output

    def test_end_to_end_no_group_column(self):
        data = {0: {'facility_type': 'b', 'outstanding': 70,
                    'transactions': {0: {'transaction_type': 'a', 'outstanding': 5},
                                     1: {'transaction_type': 'b', 'outstanding': 65}}},
                1: {'facility_type': 'a', 'outstanding': 135,
                    'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                     3: {'transaction_type': 'b', 'outstanding': 74}}},
                2: {'facility_type': 'b', 'outstanding': 211,
                    'transactions': {4: {'transaction_type': 'b', 'outstanding': 36},
                                     5: {'transaction_type': 'a', 'outstanding': 96},
                                     6: {'transaction_type': 'a', 'outstanding': 79}}},
                3: {'facility_type': 'a', 'outstanding': 209,
                    'transactions': {7: {'transaction_type': 'c', 'outstanding': 77},
                                     8: {'transaction_type': 'a', 'outstanding': 39},
                                     9: {'transaction_type': 'a', 'outstanding': 93}}}}

        expected_output = {'b': {'facility_type': 'b', 'outstanding': 281,
                                 'transactions': {'': {'transaction_type': 'a', 'outstanding': 281}}},
                           'a': {'facility_type': 'a', 'outstanding': 344,
                                 'transactions': {'': {'transaction_type': 'b', 'outstanding': 344}}}}

        instructions = [('facility_type',), ('outstanding', au.sum), {'transactions': [('outstanding', au.sum)]}]
        output = DictAggregation(data).aggregate(data, instructions)
        assert output == expected_output

    def test_end_to_end_no_portal(self):
        data = {0: {'facility_type': 'b', 'outstanding': 70,
                    'transactions': {0: {'transaction_type': 'a', 'outstanding': 5},
                                     1: {'transaction_type': 'b', 'outstanding': 65}}},
                1: {'facility_type': 'a', 'outstanding': 135,
                    'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                     3: {'transaction_type': 'b', 'outstanding': 74}}},
                2: {'facility_type': 'b', 'outstanding': 211,
                    'transactions': {4: {'transaction_type': 'b', 'outstanding': 36},
                                     5: {'transaction_type': 'a', 'outstanding': 96},
                                     6: {'transaction_type': 'a', 'outstanding': 79}}},
                3: {'facility_type': 'a', 'outstanding': 209,
                    'transactions': {7: {'transaction_type': 'c', 'outstanding': 77},
                                     8: {'transaction_type': 'a', 'outstanding': 39},
                                     9: {'transaction_type': 'a', 'outstanding': 93}}}}

        expected_output = {'b': {'facility_type': 'b', 'outstanding': 281,
                                 'transactions': {0: {'transaction_type': 'a', 'outstanding': 5},
                                                  1: {'transaction_type': 'b', 'outstanding': 65}}},
                           'a': {'facility_type': 'a', 'outstanding': 344,
                                 'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                                  3: {'transaction_type': 'b', 'outstanding': 74}}}}


        instructions = [('facility_type',), ('outstanding', au.sum)]
        output = DictAggregation(data).aggregate(data, instructions)
        assert output == expected_output

    def test_end_to_end_empty_sub_record(self):
        data = {0: {'facility_type': 'b', 'outstanding': 70,
                    'transactions': {0: {'transaction_type': 'a', 'outstanding': 5},
                                     1: {'transaction_type': 'b', 'outstanding': 65}}},
                1: {'facility_type': 'a', 'outstanding': 135,
                    'transactions': {2: {'transaction_type': 'b', 'outstanding': 61},
                                     3: {'transaction_type': 'b', 'outstanding': 74}}},
                2: {'facility_type': 'b', 'outstanding': 211,
                    'transactions': {4: {'transaction_type': 'b', 'outstanding': 36},
                                     5: {'transaction_type': 'a', 'outstanding': 96},
                                     6: {'transaction_type': 'a', 'outstanding': 79}}},
                3: {'facility_type': 'a', 'outstanding': 209,
                    'transactions': {}}}

        expected_output = {'b': {'facility_type': 'b', 'outstanding': 281,
                                 'transactions':
                                     {'b': {'transaction_type': 'b', 'outstanding': 101},
                                      'a': {'transaction_type': 'a', 'outstanding': 180}}},
                           'a': {'facility_type': 'a', 'outstanding': 344,
                                 'transactions':
                                     {'b': {'transaction_type': 'b', 'outstanding': 135}}}}


        instructions = [('facility_type',), ('outstanding', au.sum), {'transactions': [('transaction_type',),
                                                                                      ('outstanding', au.sum)]}]
        output = DictAggregation(data).aggregate(data, instructions)
        assert output == expected_output
