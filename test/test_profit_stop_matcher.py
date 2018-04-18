'''
Created on Jan 22, 2018

@author: ckubudi
'''

import unittest
import pandas as pd
import numpy as np
from profit_stop_matcher import Profit_Stop_Matcher

class Test(unittest.TestCase):

    def test_stop_matcher(self):
        #creates a matcher with 10% trailing profit 
        matcher=Profit_Stop_Matcher(999.0, 0.10, 3)
        
        weights=np.array([0.25,0.25,0.25,0.25])
        returns=np.array([1.00,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'weight should be equal')
        
        returns=np.array([0.90,1.00,1.00,1.00])
        #first specialist should be stopped
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], 0.0, 'specialist should be stopped')
        
        matcher.reset_trailing()
        
        weights=np.array([0.25,0.25,0.25,0.25])
        returns=np.array([1.10,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'weight should be equal')
        
        #should not stop
        returns=np.array([1.00,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'weight should be equal')
        
        #should stop
        returns=np.array([0.96,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'specialist should be stopped')
        
    def test_profit_matcher(self):
        #creates a matcher with 10% trailing profit 
        matcher=Profit_Stop_Matcher(0.10, 999.0, 3)
        
        weights=np.array([0.25,0.25,0.25,0.25])
        returns=np.array([1.05,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'weight should be equal')
        
        weights=np.array([0.25,0.25,0.25,0.25])
        returns=np.array([1.10,1.00,1.00,1.00])
        matcher_weights=matcher.new_return(weights, returns)
        self.assertEqual(matcher_weights[0], weights[0], 'specialist should be profited')
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()