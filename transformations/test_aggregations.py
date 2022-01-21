import unittest
import pandas as pd
import aggregations


class TestAggregations(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'A': ['a', 'b', None]})

    def test_missing(self):
        df = self.df
        df_aggregate = aggregations.count_per_group(df, ['A'])
        self.assertEqual(len(df_aggregate), len(df))

    def test_input_type(self):
        df = self.df
        with self.assertRaises(TypeError):
            aggregations.count_per_group((df, 'A'))

    def test_nonvalid_column(self):
        df = self.df
        with self.assertRaises(KeyError):
            aggregations.count_per_group(df, ['B'])


if __name__ == '__main__':
    unittest.main()
