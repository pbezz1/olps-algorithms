'''
Created on Nov 19, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np

#Searches given historical dataframe for similar price windows
#and returns the next step for each of them
#current_window: current past window
#historical df: dataframe with returns for each asset
#window_size: size of the window to search
#c_threshold: minimum correlation to recognize similar patterns
def process_similar_windows(current_window, historical_df, window_size, c_threshold):
    historical_list = historical_df.iloc[:,historical_df.columns != 'date'].values.flatten()
    current_window=np.asarray(current_window)
    
    similar_next_steps = []

    experts_num = len(historical_df.columns)-1    
    values_window=experts_num*window_size
    it_window_start=0
    it_window_end=values_window
    
    while(it_window_end <= len(historical_list)-experts_num):
        it_window = historical_list[it_window_start:it_window_end]
        
        if(np.corrcoef(current_window, it_window)[0,1] >= c_threshold):
            next_step=historical_list[it_window_end:it_window_end+experts_num]
            for x in next_step:
                similar_next_steps.append(x)
        
        it_window_start+=experts_num
        it_window_end+=experts_num
    
    return similar_next_steps



def find_best_cbal(forecast):
    #to be implemented
    pass
    