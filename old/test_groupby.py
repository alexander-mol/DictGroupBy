import random
import time
import unittest

from old import dict_groupby


class TestDictGroupBy(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        self.sut = dict_groupby

    def generate_transaction(self):
        return {
            'transaction_type': random.choice(['a', 'b', 'c']),
            'outstanding': random.randint(0, 100)
        }

    def generate_facility(self):
        num_transactions = random.randint(1, 3)
        transactions = {}
        outstanding = 0
        for i in range(num_transactions):
            transactions[i] = self.generate_transaction()
            outstanding += transactions[i]['outstanding']

        return {
            'facility_type': random.choice(['a', 'b', 'c']),
            'outstanding': outstanding,
            'transactions': transactions
        }

    def generate_facilities(self, num):
        out = {}
        for i in range(num):
            out[i] = self.generate_facility()
        return out

    def generate_record(self):
        return {
            'gcol1': random.choice(['a', 'b', 'c']), 'gcol2': random.choice(['a', 'b', 'c']),
            'gcol3': random.choice(['a', 'b', 'c']), 'vcol1': random.randint(0, 100), 'vcol2': random.random(),
            'vcol3': random.randint(0, 2)
        }

    def test_hierarchical_groupby(self):
        input_set = self.generate_facilities(4)
        group_columns = ['facility_type', {'transactions': 'transaction_type'}]
        print(input_set)
        self.sut.DictGroupBy(input_set, group_columns)

    def test_groupby_and_sum_speed(self):
        data = {}
        for i in range(100000):
            data[i] = self.generate_record()
        print('Generated data.')
        group_columns = ['gcol1', 'gcol2', 'gcol3']

        t0 = time.time()
        gb = dict_groupby.GroupByObj(data, group_columns)
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