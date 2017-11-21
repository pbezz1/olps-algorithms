'''
Created on Nov 6, 2017

@author: ckubudi
'''
import unittest
import multiplicative_weigths as mw 
import pandas as pd
import numpy as np
from datetime import datetime

class Test(unittest.TestCase):

    #Testing if the returns are exactly as expected
    def test_returns(self):
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 1.0 , 0.5), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 2.0 , 1.0),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(), -0.5 , -1.0)])
        returns_df.columns = ['date',"asset1","asset2"]
        
        eta=1.0
        result_df = mw.multiplicative_weights(returns_df, eta, 1, returns_df)
        
        weight = [1.0/2] * 2
        expected_returns = [0] * len(returns_df)
        expected_returns[0] = (weight[0] * returns_df.loc[0,'asset1']) + (weight[1] * returns_df.loc[0,'asset2'])
        
        self.assertAlmostEqual(expected_returns[0], result_df['result'][0], 2, "first return is wrong")
        
        #the update vec should be the returns + 1
        weight = mw.multiplicative_weigths_exp_update([2.0, 1.5], eta, weight, 2)
        expected_returns[1] = (weight[0] * returns_df.loc[1,'asset1']) + (weight[1] * returns_df.loc[1,'asset2'])
        
        self.assertAlmostEqual(expected_returns[1], result_df['result'][1], 2, "second return is wrong")
        
        #the update vec should be the returns + 1
        weight = mw.multiplicative_weigths_exp_update([3.0, 2.0], eta, weight, 2)
        expected_returns[2] = (weight[0] * returns_df.loc[2,'asset1']) + (weight[1] * returns_df.loc[2,'asset2'])
        
        self.assertAlmostEqual(expected_returns[2], result_df['result'][2], 2, "third return is wrong")
    
    
    #Testing the direction of weights with negative eta
    def test_neg_eta(self):
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 1.0 , 0.5), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 0.5),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(), 1.0 , 0.5)])
        returns_df.columns = ['date',"asset1","asset2"]
        
        eta=-0.5
        result_df = mw.multiplicative_weights(returns_df, eta, 1, returns_df)
        
        res_return=result_df['result']
        delta_1 = res_return[1] - res_return[0]
        delta_2 = res_return[2] - res_return[1]
        
        self.assertTrue(delta_1 < 0.0, "weights didnt go to right direction")
        self.assertTrue(delta_2 < 0.0, "weights didnt go to right direction")
        
    #comparing eta evolutions    
    def test_comp_eta(self):
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 1.0 , 0.5), 
                                          (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 0.5),
                                          (datetime.strptime('2017-10-03', "%Y-%m-%d").date(), 1.0 , 0.5)])
        returns_df.columns = ['date',"asset1","asset2"]
        
        
        eta_1 = 0.75
        eta_2 = 1.75
        
        result_df_1 = mw.multiplicative_weights(returns_df, eta_1, 1, returns_df)
        result_df_2 = mw.multiplicative_weights(returns_df, eta_2, 1, returns_df)

        res_return_1 = result_df_1['result']
        res_return_2 = result_df_2['result']
        
        delta_0=res_return_1[0]-res_return_2[0]
        delta_1=res_return_1[1]-res_return_2[1]
        delta_2=res_return_1[2]-res_return_2[2]
        
        self.assertTrue(delta_0 = 0, 'first round update is wrong')
        self.assertTrue(delta_1 < 0, 'learning rate is not working')
        self.assertTrue(delta_2 < 0, 'learning rate is not working')
    
               
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()