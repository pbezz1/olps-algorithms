'''
Created on Nov 25, 2017

@author: ckubudi
'''
import numpy as np
import pandas as pd
from datetime import datetime


class Algorithm(object):
    
    def __init__(self):
        pass
    
    def before_backtest(self, data):
        """to do before backtest
        :data: dataframe with returns and dates
        """
        pass 
    
    
    def update_weights(self, current_index, current_weights, data):
        """ Update the weights
        """
        return current_weights
    
    @staticmethod
    def getUCRP_weights(specialists_num):
        weights = [1.0/specialists_num] * specialists_num
        return weights
    
    def run(self, data):
        """Runs the algorithm
        :data: dataframe with each column representing a specialist, except for the first one that is the date        
        """
        columns = ['date','weights','result']
        temp = [(datetime.now().date(),[],0.0)] * len(data)  
        result = pd.DataFrame(temp, columns=columns)
        
        #gets the number of specialists and set the initial gains vector
        specialists_num=len(data.columns)-1
        weights_vec=self.getUCRP_weights(specialists_num)
        
        self.before_backtest(data)
        
        for index, row in data.iterrows():
            balanced_return=0.0
            for specialist in range(specialists_num):
                balanced_return = balanced_return + (weights_vec[specialist]*data.get_value(index,data.columns[specialist+1]))
            
            result.set_value(index, 'date', row['date'])    
            result.set_value(index, 'weights', weights_vec)
            result.set_value(index, 'result', balanced_return)
                            
            weights_vec = self.update_weights(index, weights_vec, data.iloc[0:index+1,:])
    
        return result