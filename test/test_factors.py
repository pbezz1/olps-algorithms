'''
Created on Dec 8, 2017

@author: ckubudi
'''
import unittest
import factors
import datetime
import pandas as pd

class Test(unittest.TestCase):


    def testMomentum(self):
        numdays=10
        base = datetime.datetime.today()
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
        
        prices = pd.DataFrame([(5.0,2.5),
                               (4.0,2.0),
                               (2.5,5.0),
                               (2.0,4.0),])
        
        actual_factor = factors.momentum(prices, 0, 2)
        for factor in actual_factor.loc[:,0]:
            self.assertAlmostEqual(factor, 0.5, 3, "factor not working")
        for factor in actual_factor.loc[:,1]:
            self.assertAlmostEqual(factor, 2.0, 3, "factor not working")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMomentum']
    unittest.main()