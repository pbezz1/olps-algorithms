'''
Created on Nov 20, 2017

@author: ckubudi
'''
import unittest
import factor_portfolio as fp
import pandas as pd
import numpy as np
from datetime import datetime

class Test(unittest.TestCase):

    def test_create_factor_portfolio(self):
            return_df = pd.DataFrame([(datetime.strptime('2017-10-02', "%Y-%m-%d").date(),0.20,0.05,0.10),
                                              (datetime.strptime('2017-10-03', "%Y-%m-%d").date(),0.05,0.10,0.20)],
                                     columns=['date','ASSET1','ASSET2','ASSET3'])
            factor_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),10,9,8), 
                                              (datetime.strptime('2017-10-02', "%Y-%m-%d").date(),np.NaN,np.NaN,10),
                                              (datetime.strptime('2017-10-03', "%Y-%m-%d").date(),9,10,8)],
                                     columns=['date','ASSET1','ASSET2','ASSET3'])
            
            (df,df_portfolios) = fp.create_factor_portfolio(factor_df, return_df, 2, 1)
            
            
            #standart portfolio
            self.assertEquals(df_portfolios['portfolio'][0],['ASSET1','ASSET2'],'portfolio not matching')
            self.assertAlmostEqual(df['return'][0], 0.125, 3, 'portfolio return not matching')
            
            #missing one asset portfolio
            self.assertEquals(df_portfolios['portfolio'][1],['ASSET3'],'portfolio not matching') 
            self.assertAlmostEqual(df['return'][1], 0.20, 3, 'portfolio return not matching')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()