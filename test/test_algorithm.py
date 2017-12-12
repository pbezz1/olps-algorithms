'''
Created on Dec 5, 2017

@author: ckubudi
'''
import unittest
from algorithm import Algorithm
from datetime import datetime

class Test(unittest.TestCase):

    def test_rebalance_monthly(self):
        algorithm = Algorithm()
        algorithm.rebalance_period='monthly'
        algorithm.rebalance_window=1
        
        date=datetime.strptime('2017-10-03', "%Y-%m-%d").date()
        
        actual_next_date = algorithm.getNextRebalanceDate(date)
        expected_next_date = datetime.strptime('2017-11-01', "%Y-%m-%d").date()
        
        self.assertEqual(actual_next_date, expected_next_date, 'wrong date')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRebalanceMonthly']
    unittest.main()