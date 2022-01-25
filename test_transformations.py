import unittest
import pandas as pd

from main import count_apps


class TestAggregations(unittest.TestCase):
    def setUp(self):
        df_testdata = pd.read_csv('test_data.csv', sep=',')
        df = count_apps(df_testdata)
        self.df = df[df['dato'] ==  '2022-20-01']

    def test_prodcount(self):
        df = self.df
        antall_apper = df[(df['env'] == 'prod')]['antall_apper'].sum()
        self.assertTrue(antall_apper == 3)

    def test_devcount(self):
        df = self.df
        antall_apper = df[(df['env'] == 'dev')]['antall_apper'].sum()
        self.assertTrue(antall_apper == 3)

    def test_cloud_count(self):
        df = self.df
        antall_apper = df[df['datacenter'] == 'gcp']['antall_apper'].sum()
        self.assertTrue(antall_apper == 2)

    def test_onprem_count(self):
        df = self.df
        antall_apper = df[df['datacenter'] == 'on_prem']['antall_apper'].sum()
        self.assertTrue(antall_apper == 4)


if __name__ == '__main__':
    unittest.main()
