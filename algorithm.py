'''
Created on Nov 25, 2017

@author: ckubudi
'''
import numpy as np
import pandas as pd
import math
import datetime
from dateutil.relativedelta import relativedelta


class Algorithm(object):
    
    def __init__(self):
        self.weights_vec=[]
        self.specialists_num=0
        self._rebalance_window=1
        self._rebalance_period='daily'
        self._filter=None
        pass
    
    def before_backtest(self, data):
        """to do before backtest
        :data: dataframe with returns and dates
        """
        #gets the number of specialists and set the initial gains vector
        self.weights_vec=self.getUCRP_weights(self.specialists_num)
        
        return data 
    
    
    def update_weights(self, current_index, current_weights, data):
        """ Update the weights
        """
        return current_weights
    
    def after_backtest(self):
        """to do after backtest
        """
        pass
    
    @property
    def rebalance_window(self):
        return self._rebalance_window
    
    @rebalance_window.setter
    def rebalance_window(self, value):
        self._rebalance_window = value
    
    @property
    def rebalance_period(self):
        return self._rebalance_period

    @rebalance_period.setter
    def rebalance_period(self, value):
        if value not in ('daily', 'monthly'):
            raise ValueError('invalid rebalance period')
        else:
            self._rebalance_period = value
    
    @staticmethod
    def getUCRP_weights(specialists_num):
        weights = [1.0/specialists_num] * specialists_num
        return weights
    

    def getNextRebalanceDate(self, rebalance_date):
        if(self.rebalance_period == 'monthly'):
            rebalance_date=rebalance_date.replace(day=1)            
            return rebalance_date + relativedelta(months=+self.rebalance_window)
        else: #daily
            return rebalance_date+datetime.timedelta(days=self.rebalance_window)
       
    
    def run(self, data):
        """Runs the algorithm
        :data: dataframe with each column representing a specialist, except for the first one that is the date        
        """
        #gets the number of specialists and set the initial gains vector
        self.specialists_num=len(data.columns)

        data = self.before_backtest(data)
        
        #always rebalance on first date
        rebalance_date = data.index[0]
        cum_ret=1.0
        
        #create result dataframe
        columns = ['weights','result']
        temp = [([],0.0)] * len(data)  
        result = pd.DataFrame(temp, columns=columns, index=data.index)
        
        for index, row in data.iterrows():
            if(index >= rebalance_date):
                self.weights_vec = self.update_weights(index,self.weights_vec, data.loc[:index,:])
                cum_ret=1.0
                rebalance_date=self.getNextRebalanceDate(rebalance_date)
                
            ret=(1+np.dot(self.weights_vec, row))*cum_ret
            cum_ret=ret
            
            result.set_value(index, 'weights', self.weights_vec)
            result.set_value(index, 'result', ret)
                                
        self.after_backtest()
    
        return result