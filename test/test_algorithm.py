'''
Created on Dec 5, 2017

@author: ckubudi
'''
import unittest
import numpy as np
import pandas as pd
from algorithm import Algorithm
from datetime import datetime

class Test(unittest.TestCase):
    
    def assert_list(self, list1, list2, places):
        self.assertEqual(len(list1), len(list2), "Lists dont have the same size")
        
        for i in range(len(list1)):
            self.assertAlmostEqual(list1[i], list2[i], places, 'Element with index '+str(i)+' are not equal')

    def test_rebalance_monthly(self):
        
        algorithm_params={'rebalance_period': 'monthly','rebalance_window':1}
        algorithm = Algorithm(algorithm_params)
        
        date=datetime.strptime('2017-10-03', "%Y-%m-%d").date()
        
        actual_next_date = algorithm.getNextRebalanceDate(date)
        expected_next_date = datetime.strptime('2017-11-01', "%Y-%m-%d").date()
        
        self.assertEqual(actual_next_date, expected_next_date, 'wrong date')
    
    def assert_returns(self, df_result, expected_returns):
        self.assertEqual(3, len(df_result), 'length of result is not matching')
        real_returns=df_result['result']
        
        for i in range(len(df_result)):
            self.assertAlmostEqual(real_returns[i], expected_returns[i], 3, 'returns not matching')
    
    def test_daily_returns(self):
        algorithm_params={'rebalance_period': 'daily','rebalance_window':1,'cost':0.0}
        algorithm = Algorithm(algorithm_params)
        
        return_df = pd.DataFrame([(0.20,0.10),
                        (0.10,0.10),
                        (0.05,0.10)],
                        columns=['ASSET1','ASSET2'],
                        index=[pd.Timestamp('20171002'),
                        pd.Timestamp('20171003'),
                        pd.Timestamp('20171004')])
        return_df.index.name='date'
    
        result=algorithm.run(return_df)
        
        df_result=result.data
        
        self.assert_returns(df_result, [0.15,0.10,0.075])
        
        
    def test_daily_negative_returns(self):
        algorithm_params={'rebalance_period': 'daily','rebalance_window':1,'cost':0.0}
        algorithm = TestAlgorithmNegWeights(algorithm_params)
        
        return_df = pd.DataFrame([(0.20,0.10),
                        (0.10,0.10),
                        (0.05,0.20)],
                        columns=['ASSET1','ASSET2'],
                        index=[pd.Timestamp('20171002'),
                        pd.Timestamp('20171003'),
                        pd.Timestamp('20171004')])
        return_df.index.name='date'
        result=algorithm.run(return_df)
        df_result=result.data
        self.assert_returns(df_result, [0.15,0.05,-0.05])
        
        return_df = pd.DataFrame([(0.00,0.20),
                        (0.00,0.10),
                        (0.00,0.30)],
                        columns=['ASSET1','ASSET2'],
                        index=[pd.Timestamp('20171002'),
                        pd.Timestamp('20171003'),
                        pd.Timestamp('20171004')])
        return_df.index.name='date'
        result=algorithm.run(return_df)
        df_result=result.data
        self.assert_returns(df_result, [-0.1,-0.05,-0.15])
    
    def test_calculate_turnover(self):
        algorithm = Algorithm()
        
        #simple weights - no change in weights
        current_weights=np.array([0.5,0.5])
        last_weights=np.array([0.5,0.5])
        current_individual_returns=np.array([1.1,1.1])
        result=algorithm.calculate_turnover2(current_weights, last_weights, current_individual_returns, iteration=999)
        self.assertEqual(result,0.0)
        
        #simple weights - change with same returns
        current_weights=np.array([0.5,0.5])
        last_weights=np.array([0.6,0.4])
        current_individual_returns=np.array([1.0,1.0])
        result=algorithm.calculate_turnover2(current_weights, last_weights, current_individual_returns, iteration=999)
        self.assertAlmostEqual(result,0.2,3)

        #simple weights - change with same returns
        current_weights=np.array([0.5,0.5])
        last_weights=np.array([0.6,0.4])
        current_individual_returns=np.array([1.0,1.0])
        result=algorithm.calculate_turnover2(current_weights, last_weights, current_individual_returns, iteration=999)
        self.assertAlmostEqual(result,0.2,3)
        
        #simple weights - no change but different returns
        current_weights=np.array([0.5,0.5])
        last_weights=np.array([0.5,0.5])
        current_individual_returns=np.array([1.2,1.0])
        result=algorithm.calculate_turnover2(current_weights, last_weights, current_individual_returns, iteration=999)
        self.assertAlmostEqual(result,0.1,3)
    

    def test_calculate_turnover_negative_weights(self):
        algorithm = Algorithm()
        
        #simple weights - no change in weights
        current_weights=np.array([0.6,-0.3,0.4])
        last_weights=np.array([0.6,-0.3,0.4])
        current_individual_returns=np.array([1.1,1.1,1.0])
        result=algorithm.calculate_turnover2(current_weights, last_weights, current_individual_returns, iteration=999)
        self.assertAlmostEqual(result,0.06,3)
        
    def test_trim_back(self):
        algorithm = Algorithm()

        arr=np.array([None, None, 2, 3 ,5, None])
        actual_res=algorithm.trim_back(arr, None)
        expected_res=[None, None, 2, 3 ,5]
        self.assert_list(actual_res, expected_res, 2)

        arr=np.array([None, None, 2, 3 ,5, None, None, None])
        actual_res=algorithm.trim_back(arr, None)
        expected_res=[None, None, 2, 3 ,5]
        self.assert_list(actual_res, expected_res, 2)

        arr=np.array([None, None, 2, 3 ,5])
        actual_res=algorithm.trim_back(arr, None)
        expected_res=[None, None, 2, 3 ,5]
        self.assert_list(actual_res, expected_res, 2)
        
        arr=np.array([2, None ,None])
        actual_res=algorithm.trim_back(arr, None)
        expected_res=[2]
        self.assert_list(actual_res, expected_res, 2)
        
        arr=np.array([None, None, None])
        actual_res=algorithm.trim_back(arr, None)
        expected_res=[]
        self.assert_list(actual_res, expected_res, 2)
    
    def test_trim_front(self):
        algorithm = Algorithm()

        arr=np.array([None, 2, 3 ,5, None])
        actual_res=algorithm.trim_front(arr, None)
        expected_res=[2, 3 ,5, None]
        self.assert_list(actual_res, expected_res, 2)

        arr=np.array([None, None, 2, 3 ,5, None])
        actual_res=algorithm.trim_front(arr, None)
        expected_res=[2, 3 ,5, None]
        self.assert_list(actual_res, expected_res, 2)

        arr=np.array([2, 3 ,5, None])
        actual_res=algorithm.trim_front(arr, None)
        expected_res=[2, 3 ,5, None]
        self.assert_list(actual_res, expected_res, 2)
        
        arr=np.array([None ,None, 2])
        actual_res=algorithm.trim_front(arr, None)
        expected_res=[2]
        self.assert_list(actual_res, expected_res, 2)
        
        arr=np.array([None, None, None])
        actual_res=algorithm.trim_front(arr, None)
        expected_res=[]
        self.assert_list(actual_res, expected_res, 2)
        
    def test_trim_result(self):
        algorithm = Algorithm()
        
        result=[0.0,0.0,1.0,2.0,0.0]
        weights_list=[[0.0,0.0],[0.0,0.0],[0.5,0.5],[0.5,0.5],[0.0,0.0]]
        index=pd.Index([pd.Timestamp('20171001'),
                pd.Timestamp('20171002'),
                pd.Timestamp('20171003'),
                pd.Timestamp('20171004'),
                pd.Timestamp('20171005')])
        
        trim_result,trim_wegihts_list,trim_idx=algorithm.trim_result(result, weights_list, index)
        
        self.assert_list(trim_result, [1.0,2.0], 3)
        self.assertEqual(len(trim_wegihts_list), 2)
        self.assert_list(trim_wegihts_list[0],[0.5,0.5],3)
        self.assert_list(trim_wegihts_list[1],[0.5,0.5],3)
        self.assertEqual(len(trim_idx), 2)
        self.assertEqual(trim_idx[0], pd.Timestamp('20171003'))
        self.assertEqual(trim_idx[1], pd.Timestamp('20171004'))
        
    def test_custom_normalization(self):
        strategy=Algorithm()
        
        weights=pd.Series([0.25,0.25,0.0])
        result=strategy.custom_normalize(weights)
        expected=pd.Series([0.5,0.5,0.0])
        self.assert_list(result, expected, 3)
        
        weights=pd.Series([0.25,0.25,-0.25])
        result=strategy.custom_normalize(weights)
        expected=pd.Series([0.5,0.5,-0.5])
        self.assert_list(result, expected, 3)
        
        weights=pd.Series([-0.25,-0.25,0.25])
        result=strategy.custom_normalize(weights)
        expected=pd.Series([0.0,0.0,0.0])
        self.assert_list(result, expected, 3)
        
        weights=pd.Series([-0.25,-0.25,0.0])
        result=strategy.custom_normalize(weights)
        expected=pd.Series([0.0,0.0,-0.0])
        self.assert_list(result, expected, 3)
        
        weights=pd.Series([0.0,0.0,0.0])
        result=strategy.custom_normalize(weights)
        expected=pd.Series([0.0,0.0,-0.0])
        self.assert_list(result, expected, 3)
        
class TestAlgorithmNegWeights(Algorithm):
    def __init__(self, params):
        Algorithm.__init__(self, params)

    def update_weights(self, current_index, current_weights, data):
        #alternating weights
        weights = np.empty((len(current_weights),))
        weights[::2] = 1
        weights[1::2] = -0.5
        weights=self.custom_normalize(weights)
        return weights
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRebalanceMonthly']
    unittest.main()