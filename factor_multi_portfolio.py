'''
Created on Dec 7, 2017

@author: ckubudi
'''
import numpy as np
from factor_portfolio import Factor_Portfolio
from queue import Queue

class Factor_Multi_Portfolio(Factor_Portfolio):
    
    def __init__(self, assets_list, factor_name, portfolio_size, n_portfolios):
        """Algorithm similar to factor portfolio, but produces the ranking based on 12 different portfolios
        :n_portfolios: number of portfolios to be considered
        """
        super(Factor_Multi_Portfolio, self).__init__(assets_list, factor_name, portfolio_size)
        self._n_portfolios=n_portfolios
    
    @property
    def name(self):
        return "Multi Factor "+self._factor_name
    
    def before_backtest(self, data):
        if(self.rebalance_period == 'daily'):
            raise ValueError("Facor Multi Portfolio strategy doesn't support daily updates")
        data=super(Factor_Multi_Portfolio, self).before_backtest(data)
        self._p=self.rebalance_window
        self._queue=Queue(maxsize=self._n_portfolios)
        for idx in range(self._n_portfolios):
            algorithm = Factor_Portfolio(self._assets_list, self._factor_name, self.portfolio_size)
            
        self.rebalance_window=1
        self._periods=0
        self._first_operation_date=None
        return data
    
    def update_weights(self, current_index, current_weights, data):
        current_date=data.index[len(data)-1]
        
        #current regular rebalance
        weights = super(Factor_Multi_Portfolio,self).update_weights(current_index, current_weights, data)
        self._periods+=1
        if(self._queue.full()):
            #dequeue element
            self._queue.get()
        self._queue.put(weights)
        
        if(self._queue.full()):
            if(self._first_operation_date is None):
                self._first_operation_date = current_index
            return self.average_portfolios(self._queue)
        else:
            return [0.]*self.specialists_num
    
    def after_backtest(self):
        #crop results to match start of portfolio
        self._result=self._result[self._result.index > self._first_operation_date]