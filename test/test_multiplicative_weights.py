'''
Created on Nov 6, 2017

@author: ckubudi
'''
import unittest
from multiplicative_weigths import Multiplicative_Weights
import pandas as pd
from datetime import datetime

class Test(unittest.TestCase):
    
    #Test normalize function
    def test_normalize(self):
        vec1 = [2.0, 3.0, 5.0]
        vec1 = Multiplicative_Weights.normalize(vec1)
        exp_vec1 = [0.2,0.3,0.5]
        
        for i in range(0,len(vec1)):
            self.assertAlmostEqual(exp_vec1[i], vec1[i], 2, "normalization not working")
        
        vec2 = [0.02,0.03,0.05]
        vec2 = Multiplicative_Weights.normalize(vec2)
        exp_vec2 = [0.2,0.3,0.5]
        
        for i in range(0,len(vec2)):
            self.assertAlmostEqual(exp_vec2[i], vec2[i], 2, "normalization not working")
    


    #Testing if the returns are exactly as expected
    def test_returns(self):
        index=[datetime.strptime('2017-10-01', "%Y-%m-%d"),datetime.strptime('2017-10-02', "%Y-%m-%d"),datetime.strptime('2017-10-03', "%Y-%m-%d")]
        returns_df = pd.DataFrame([(1.0 , 0.5), 
                                          ( 2.0 , 1.0),
                                          ( -0.5 , -1.0)]
        ,index=index
        ,columns=["asset1","asset2"])
        returns_df.index.name='date'
        
        eta=1.0
        algorithm =Multiplicative_Weights(eta)
        algorithm.rebalance_window=1
        result_df = algorithm.run(returns_df).data
        
        weight = [1.0/2] * 2
        expected_returns = [0] * len(returns_df)
        expected_returns[0] = (weight[0] * returns_df.loc[index[0],'asset1']) + (weight[1] * returns_df.loc[index[0],'asset2'])
        
        self.assertAlmostEqual(expected_returns[0], result_df['result'][0], 2, "first return is wrong")
        
        #the update vec should be the returns + 1
        weight = algorithm.multiplicative_weigths_exp_update([2.0, 1.5], weight, 2)
        expected_returns[1] = (weight[0] * returns_df.loc[index[1],'asset1']) + (weight[1] * returns_df.loc[index[1],'asset2'])
        
        self.assertAlmostEqual(expected_returns[1], result_df['result'][1], 2, "second return is wrong")
        
        #the update vec should be the returns + 1
        weight = algorithm.multiplicative_weigths_exp_update([3.0, 2.0], weight, 2)
        expected_returns[2] = (weight[0] * returns_df.loc[index[2],'asset1']) + (weight[1] * returns_df.loc[index[2],'asset2'])
        
        self.assertAlmostEqual(expected_returns[2], result_df['result'][2], 2, "third return is wrong")
    
    
    #Testing the direction of weights with negative eta
    def test_neg_eta(self):
        index=[datetime.strptime('2017-10-01', "%Y-%m-%d"),datetime.strptime('2017-10-02', "%Y-%m-%d"),datetime.strptime('2017-10-03', "%Y-%m-%d")]
        returns_df = pd.DataFrame([(1.0 , 0.5), 
                                          (1.0 , 0.5),
                                          (1.0 , 0.5)],
                                  index=index,
                                  columns =  ["asset1","asset2"])
        returns_df.index.name='date'

        
        eta=-0.5
        algorithm =Multiplicative_Weights(eta)
        result_df = algorithm.run(returns_df).data
        
        res_return=result_df['result']
        delta_1 = res_return[1] - res_return[0]
        delta_2 = res_return[2] - res_return[1]
        
        self.assertTrue(delta_1 < 0.0, "weights didnt go to right direction")
        self.assertTrue(delta_2 < 0.0, "weights didnt go to right direction")
        
    #comparing eta evolutions    
    def test_comp_eta(self):
        index=[datetime.strptime('2017-10-01', "%Y-%m-%d"),datetime.strptime('2017-10-02', "%Y-%m-%d"),datetime.strptime('2017-10-03', "%Y-%m-%d")]
        returns_df = pd.DataFrame([(1.0 , 0.5), 
                                          (1.0 , 0.5),
                                          (1.0 , 0.5)],
                                  index=index,
                                  columns=["asset1","asset2"])
        returns_df.index.name='date'
        
        
        eta_1 = 0.75
        eta_2 = 1.75
        algorithm1=Multiplicative_Weights(eta_1)
        algorithm2=Multiplicative_Weights(eta_2)

        
        result_df_1 = algorithm1.run(returns_df).data
        result_df_2 = algorithm2.run(returns_df).data

        res_return_1 = result_df_1['result']
        res_return_2 = result_df_2['result']
        
        delta=res_return_1[0]-res_return_2[0]
        delta_1=res_return_1[1]-res_return_2[1]
        delta_2=res_return_1[2]-res_return_2[2]
        
        self.assertEquals(0,delta)
        self.assertTrue(delta_1 < 0, 'learning rate is not working')
        self.assertTrue(delta_2 < 0, 'learning rate is not working')
    
               
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()