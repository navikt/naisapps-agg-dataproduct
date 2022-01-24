import unittest
import pandas as pd
import aggregations


class TestAggregations(unittest.TestCase):
    def setUp(self):
        self.df_raw = pd.read_csv('test_data.csv', separator=',')
        df = aggregate(df_raw)
        self.dato = '2022-01-01'


    def test_prodcount(self):
        df = self.df
        antall_apper = df[(df['dato']==self.dato) & (df['env']=='prod')]['antall_apper']
        self.assertEqual(antall_apper==3)


    def test_cloud_count(self):
        df = self.df
        antall_apper = df[(df['dato']==self.dato) & (df['datacenter']=='gcp')]['antall_apper']
        self.assertEqual(antall_apper==3)


    def test_onprem_count(self):
        df = self.df
        antall_apper = df[(df['dato']==self.dato) & (df['datacenter']=='onprem')]['antall_apper']
        self.assertEqual(antall_apper==3)



if __name__ == '__main__':
    unittest.main()
