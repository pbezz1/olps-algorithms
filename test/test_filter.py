'''
Created on Dec 5, 2017

@author: ckubudi
'''
import unittest
from filter import Filter
import datetime

class Test(unittest.TestCase):

    def test_filter(self):
        filter = Filter(file_path='../../test_data/filter/Test.csv')
        
        date = datetime.datetime.strptime('1/3/2002', "%m/%d/%Y").date() 
        
        self.assertTrue(filter.is_white_listed('ABEV3',date), 'filter not working')
        self.assertFalse(filter.is_white_listed('NEXISTE4',date), 'filter not working')
        
        """date = datetime.datetime.strptime("1/1/2000", "%m/%d/%Y").date() 
        'self.assertRaises(KeyError, filter.is_white_listed('TEST',date))
        """
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()