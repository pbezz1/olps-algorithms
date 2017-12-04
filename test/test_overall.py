'''
Created on Nov 3, 2017

@author: ckubudi
'''
import unittest
import load_factors as lf
from factor_portfolio import Factor_Portfolio
import tools
import pickle
import os

class Test(unittest.TestCase):

    def pre_process_algorithm(self):
        factors = ['price_to_book']
        assets_list=lf.load_assets(factors, '../../data/')
        returns_df=lf.create_factor_df(assets_list,'return',False)
        
        rebalance_window=60
        algorithm = Factor_Portfolio(assets_list, 'price_to_book', 10, rebalance_window)
        pickle.dump(algorithm, open('../../dump/price_to_book_algorithm.p', 'wb'))
        pickle.dump(returns_df, open('../../dump/returns.p', 'wb'))

    def test_factor_portfolios(self):  
        algorithm = pickle.load(open('../../dump/price_to_book_algorithm.p', 'rb'))
        returns_df = pickle.load(open('../../dump/returns.p', 'rb'))
        data = algorithm.run(returns_df)
        
        print('end')
        
        tools.plot_cumulative_returns(data)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()