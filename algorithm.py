'''
Created on Nov 25, 2017

@author: ckubudi
'''
import numpy as np
import pandas as pd
import math
import datetime
from dateutil.relativedelta import relativedelta
from algorithm_result import AlgorithmResult


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
        
        return data[data.index > self.start_date] 
    
    
    def update_weights(self, current_index, current_weights, data):
        """ Update the weights
        """
        return current_weights
    
    def after_backtest(self):
        """to do after backtest
        """
        pass
    
    @property
    def name(self):
        return 'Algorithm'
    
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
       
    
    def run(self, data, start_date = None):
        """Runs the algorithm
        :data: dataframe with each column representing a specialist, except for the first one that is the date        
        """
        self.start_date= datetime.datetime.strptime(start_date, "%m/%d/%Y")
        
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
                rebalance_date=self.getNextRebalanceDate(rebalance_date)
                ret=np.dot(self.weights_vec, row)
                cum_ret=1.0+ret
            else:
                temp=(1+np.dot(self.weights_vec, row))*cum_ret
                ret=(temp-cum_ret)
                cum_ret=temp
            
            result.set_value(index, 'weights', self.weights_vec)
            result.set_value(index, 'result', ret)
                                
        self.after_backtest()
    
        return AlgorithmResult(result, self.name)