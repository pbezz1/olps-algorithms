'''
Created on Oct 28, 2017

@author: ckubudi
'''

import unittest
import load_factors as lf
import factors
import pandas as pd
import numpy as np
from asset import Asset
import datetime

class TestLoadFactors(unittest.TestCase):
    def test_load_assets(self):
        actual_assets = lf.load_assets(['test_factor1'], '../../test_data/')
        
        actual_set={}
        for asset in actual_assets:
            actual_set[asset.name]=asset
            
        self.assertTrue(actual_set.__contains__('ASSET1'), 'ASSET1 not processed')
        self.assertTrue(actual_set.__contains__('ASSET2'), 'ASSET2 not processed')

        expected_return_df = pd.DataFrame([0.,.1,-.1],index=[datetime.datetime.strptime('2017-09-30', "%Y-%m-%d").date(),
                                                          datetime.datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 
                                                          datetime.datetime.strptime('2017-10-02', "%Y-%m-%d").date()])
        expected_return_df.columns = ['return']
        expected_return_df.index.name = 'date'
        
        actual_prices_df = actual_set.get('ASSET1').get_factor('close')
        actual_return_df = factors.prices_to_returns(actual_prices_df)
        
        self.assertTrue(len(actual_return_df)==3 , 'return not matching')
        for r in range(3):
            self.assertAlmostEqual(expected_return_df['return'][r],actual_return_df['return'][r], 3,  'return not matching')
        
        expected_factor1_df = pd.DataFrame([10],index=[datetime.datetime.strptime('2017-10-01','%Y-%m-%d').date()])
        expected_factor1_df.columns = ['test_factor1']
        expected_factor1_df.index.name = 'date'

        actual_factor1_df = actual_set.get('ASSET1').get_factor('test_factor1')

        self.assertTrue(expected_factor1_df.equals(actual_factor1_df), 'factor1 not matching')
        
    
    def test_create_extra_factor(self):
        actual_assets = lf.load_assets(['test_factor1','test_factor2'], '../../test_data/')
        
        actual_set={}
        for asset in actual_assets:
            actual_set[asset.name]=asset
        
        lf.create_extra_factor(actual_assets, 'test_factor1', 'test_factor2', 'extra_factor1')
        
        extra_factor_df = actual_set['ASSET1'].get_factor('extra_factor1')
        
        self.assertIsNotNone(extra_factor_df, 'extra factor has not been created for asset1')
        
        expected_extrafactor_df = pd.DataFrame([2.0],index=[datetime.datetime.strptime('2017-10-01', "%Y-%m-%d").date()])
        expected_extrafactor_df.index.name = 'date'
        expected_extrafactor_df.columns = ['extra_factor1']
        
        self.assertTrue(extra_factor_df.equals(expected_extrafactor_df) , 'extra factor 1 is wrong for asset1')
        
        extra_factor_df = actual_set['ASSET2'].get_factor('extra_factor1') 
        
        self.assertIsNotNone(extra_factor_df, 'extra factor has not been created for asset2')
        
        self.assertEqual(len(extra_factor_df.index), 0, 'extra factor 1 is wrong for asset2')
        
     
    def test_create_factor_df(self):
        actual_assets = lf.load_assets(['test_factor1','test_factor2'], '../../test_data/')
        
        ret_df = lf.create_factor_df(actual_assets, 'close', True)
        
        expected_return_df = pd.DataFrame([(0.10,np.NaN),(-0.10,-0.10),(np.NaN,0.10)],
                                          index=[datetime.datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 
                                          datetime.datetime.strptime('2017-10-02', "%Y-%m-%d").date(),
                                          datetime.datetime.strptime('2017-10-03', "%Y-%m-%d").date()])
        expected_return_df.columns=['ASSET1','ASSET2']
        expected_return_df.index.name='date'
        
        #self.assertEquals(list(ret_df.index), list(expected_return_df.index), 'merge returns dates are wrong')
        #to do
        
        
    def test_create_momentum_factor(self):
        asset = Asset('Test')
        prices = pd.DataFrame([10,10,10,10,10,10,10,5,5,5],columns=['close'])
        numdays=len(prices)
        base = datetime.datetime.today()
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
        prices.index=date_list
        asset.add_factor('close', prices)
        
        assets_list = [asset]
        factor_name='momentum3x10'
        lf.create_momentum_factor(assets_list, 3, 10, factor_name)
        factor_df = asset.get_factor(factor_name)
        
        self.assertTrue(not factor_df.empty, "factor dont exist")
        self.assertAlmostEqual(factor_df[factor_name][0], 5./(sum([10,10,10,10,10,10,10,5,5,5])/10), 4, "factor not equal")        

if __name__ == '__main__':
    unittest.main()