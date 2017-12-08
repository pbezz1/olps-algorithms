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
        self.cost=0.0
    
    def before_backtest(self, data):
        """to do before backtest
        :data: dataframe with returns and dates
        """
        #gets the number of specialists and set the initial gains vector
        self.weights_vec=self.getUCRP_weights(self.specialists_num)
        self._last_weights=[.0]*self.specialists_num
        
        return data[data.index >= self.start_date] 
    
    
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
        if(start_date is not None):
            self.start_date= datetime.datetime.strptime(start_date, "%m/%d/%Y")
        else:
            self.start_date=data.index[0]
        #gets the number of specialists and set the initial gains vector
        self.specialists_num=len(data.columns)

        data = self.before_backtest(data)
        
        #always rebalance on first date
        rebalance_date = data.index[0]
        
        #create result_df dataframe
        columns = ['weights','result']
        temp = [([],0.0)] * len(data)  
        self._result = pd.DataFrame(temp, columns=columns, index=data.index)
        
        for index, row in data.iterrows():
            if(index >= rebalance_date):
                self.weights_vec = self.update_weights(index,self.weights_vec, data.loc[:index,:])
                rebalance_date=self.getNextRebalanceDate(rebalance_date)
                turnover = np.sum(np.abs(np.subtract(self.weights_vec, self._last_weights)))
                self._last_weights=self.weights_vec
            else:
                turnover=0.0
            
            ret=np.dot(self.weights_vec, row)-(turnover*self.cost)
            
            self._result.set_value(index, 'weights', self.weights_vec)
            self._result.set_value(index, 'result', ret)
                                
        self.after_backtest()
    
        return AlgorithmResult(self._result, self.name)