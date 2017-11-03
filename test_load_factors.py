'''
Created on Oct 28, 2017

@author: ckubudi
'''

import unittest
import load_factors as lf
import pandas as pd
import numpy as np
from datetime import datetime

class TestLoadFactors(unittest.TestCase):

    def test_load_assets(self):
        actual_assets = lf.load_assets(['test_factor1'], '../test_data/')
        
        actual_set={}
        for asset in actual_assets:
            actual_set[asset.name]=asset
            
        self.assertTrue(actual_set.__contains__('ASSET1'), 'ASSET1 not processed')
        self.assertTrue(actual_set.__contains__('ASSET2'), 'ASSET2 not processed')

        expected_return_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),0.10), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(),-0.10)])
        expected_return_df.columns = ['date','return']
        
        actual_return_df = actual_set.get('ASSET1').get_factor('return')
        
        self.assertTrue(expected_return_df.equals(actual_return_df) , 'return not matching')
        
        expected_factor1_df = pd.DataFrame([(datetime.strptime('2017-10-01','%Y-%m-%d').date(), 10)])
        expected_factor1_df.columns = ['date', 'test_factor1']

        actual_factor1_df = actual_set.get('ASSET1').get_factor('test_factor1')

        self.assertTrue(expected_factor1_df.equals(actual_factor1_df), 'factor1 not matching')
        
    
    def test_create_extra_factor(self):
        actual_assets = lf.load_assets(['test_factor1','test_factor2'], '../test_data/')
        
        actual_set={}
        for asset in actual_assets:
            actual_set[asset.name]=asset
        
        lf.create_extra_factor(actual_assets, 'test_factor1', 'test_factor2', 'extra_factor1')
        
        extra_factor_df = actual_set['ASSET1'].get_factor('extra_factor1')
        
        self.assertIsNotNone(extra_factor_df, 'extra factor has not been created for asset1')
        
        expected_extrafactor_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),2.0)])
        expected_extrafactor_df.columns = ['date','extra_factor1']
        
        self.assertTrue(extra_factor_df.equals(expected_extrafactor_df) , 'extra factor 1 is wrong for asset1')
        
        extra_factor_df = actual_set['ASSET2'].get_factor('extra_factor1') 
        
        self.assertIsNotNone(extra_factor_df, 'extra factor has not been created for asset2')
        
        self.assertEqual(len(extra_factor_df.index), 0, 'extra factor 1 is wrong for asset2')
        
     
    def test_create_factor_df(self):
        actual_assets = lf.load_assets(['test_factor1','test_factor2'], '../test_data/')
        
        ret_df = lf.create_factor_df(actual_assets, 'return', True)
        
        expected_return_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),0.10,np.NaN), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(),-0.10,-0.10),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(),np.NaN,0.10)])
        expected_return_df.columns=['date','ASSET1','ASSET2']
        
        self.assertEquals(list(ret_df['date']), list(expected_return_df['date']), 'merge returns dates are wrong')
        
    def test_create_factor_portfolio(self):
        return_df = pd.DataFrame([(datetime.strptime('2017-10-02', "%Y-%m-%d").date(),0.20,0.05,0.10),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(),0.05,0.10,0.20)],
                                 columns=['date','ASSET1','ASSET2','ASSET3'])
        factor_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),10,9,8), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(),np.NaN,np.NaN,10),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(),9,10,8)],
                                 columns=['date','ASSET1','ASSET2','ASSET3'])
        
        (df,df_portfolios) = lf.create_factor_portfolio(factor_df, return_df, 2, 1)
        
        
        #standart portfolio
        self.assertEquals(df_portfolios['portfolio'][0],['ASSET1','ASSET2'],'portfolio not matching')
        self.assertAlmostEqual(df['return'][0], 0.125, 3, 'portfolio return not matching')
        
        #missing one asset portfolio
        self.assertEquals(df_portfolios['portfolio'][1],['ASSET3'],'portfolio not matching') 
        self.assertAlmostEqual(df['return'][1], 0.20, 3, 'portfolio return not matching')
        
        
if __name__ == '__main__':
    unittest.main()