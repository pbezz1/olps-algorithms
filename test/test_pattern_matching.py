'''
Created on Nov 19, 2017

@author: ckubudi
'''
import unittest
from datetime import datetime
import pandas as pd
import numpy as np
from pattern_matching import Pattern_Matching

class Test(unittest.TestCase):


    def test_similar_window_simple(self):
        current_window=[0.1,0.2]
        window_size=1
        c_threshold=0.9
        
        #find equal window
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 0.1 , 0.2), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.0 , 1.0)])
        returns_df.columns=['date','asset1','asset2']
        
        next_steps = Pattern_Matching.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        next_step=next_steps[0]
        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
        
        #find equal but negative window
        returns_df.loc[0,'asset1'] = -0.2
        returns_df.loc[0,'asset2'] = -0.1
        
        next_steps = Pattern_Matching.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        next_step=next_steps[0]

        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
        
        #find very similar window
        returns_df.loc[0,'asset1'] = 0.55
        returns_df.loc[0,'asset2'] = 1.0
        
        next_steps = Pattern_Matching.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        next_step=next_steps[0]

        expected_next_steps=[1.0,1.0]
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
            
        #find nothing    
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(),1.0 , 1.0), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 0.1 , 0.2)])
        returns_df.columns=['date','asset1','asset2']
        
        next_step = Pattern_Matching.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        
        self.assertTrue(not next_step, "algorithm found something it should not")   
        
        
    def test_similar_window_multiple(self):
        current_window=[0.1,0.2,0.5,0.6]
        window_size=2
        c_threshold=0.9
        
        #find equal window
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 0.4 , 0.8), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.6 , 2.0), 
                                           (datetime.strptime('2017-10-03', "%Y-%m-%d").date(), 1.0 , 1.0), 
                                           (datetime.strptime('2017-10-04', "%Y-%m-%d").date(), 1.0 , 1.0)])
        returns_df.columns=['date','asset1','asset2']
        
        next_steps = Pattern_Matching.process_similar_windows(current_window, returns_df, window_size, c_threshold)
        next_step=next_steps[0]

        expected_next_steps=[1.0,1.0]
        self.assertEquals(len(next_step),len(expected_next_steps))
        for idx in range(0,len(next_step)):
            self.assertAlmostEquals(next_step[idx], expected_next_steps[idx],"algorithm didn't find similar window")
            
    def test_bcrp(self):
        data = pd.DataFrame([(1.0, 0.5),(1.0, 2.0),(1.0, 0.5),(1.0, 2.0),(1.0, 0.5),(1.0, 2.0)])
        
        bcrp = Pattern_Matching.get_bcrp(data)
        
        expected_bcrp=[0.5,0.5]
        self.assertEquals(len(expected_bcrp),len(bcrp))
        for idx in range(0,len(bcrp)):
            self.assertAlmostEquals(expected_bcrp[idx], bcrp[idx],"algorithm didn't find similar window")
         
    
    def test_run(self):
        returns_df = pd.DataFrame([(datetime.strptime('2017-10-01', "%Y-%m-%d").date(), 0.4 , 0.8), 
                                           (datetime.strptime('2017-10-02', "%Y-%m-%d").date(), 1.6 , 2.0), 
                                           (datetime.strptime('2017-10-03', "%Y-%m-%d").date(), 1.0 , 1.0), 
                                           (datetime.strptime('2017-10-04', "%Y-%m-%d").date(), 1.0 , 1.0)])
        returns_df.columns=['date','asset1','asset2']
        
        algorithm =Pattern_Matching(1,0.9)
        result=algorithm.run(returns_df)

        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()