'''
Created on Nov 19, 2017

@author: ckubudi
'''
import unittest
from datetime import datetime
import pandas as pd
import numpy as np
import pattern_matching as pm


class Test(unittest.TestCase):


    def test_similar_window_simple(self):
        current_window=[0.1,0.2]
        window_size=1
        c_threshold=0.9
        
        #find equal window
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 0.1 , 0.2), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 1.0)])
        returns_df.columns=['date','asset1','asset2']
        
        next_step = pm.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
        
        #find equal but negative window
        returns_df.loc[0,'asset1'] = -0.2
        returns_df.loc[0,'asset2'] = -0.1
        
        next_step = pm.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
        
        #find very similar window
        returns_df.loc[0,'asset1'] = 0.55
        returns_df.loc[0,'asset2'] = 1.0
        
        next_step = pm.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
            
        #find nothing    
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),1.0 , 1.0), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 0.1 , 0.2)])
        returns_df.columns=['date','asset1','asset2']
        
        next_step = pm.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        self.assertTrue(not next_step, "algorithm found something it should not")   
        
        
    def test_similar_window_multiple(self):
        current_window=[0.1,0.2,0.5,0.6]
        window_size=2
        c_threshold=0.9
        
        #find equal window
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 0.4 , 0.8), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.6 , 2.0), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 1.0), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 1.0)])
        returns_df.columns=['date','asset1','asset2']
        
        next_step = pm.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        expected_next_steps=[1.0,1.0]
        self.assertEquals(len(next_step),len(expected_next_steps))
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
            
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()