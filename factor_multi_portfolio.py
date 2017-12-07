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
                
    def before_backtest(self, data):
        if(self.rebalance_period == 'daily'):
            raise ValueError("Facor Multi Portfolio strategy doesn't support daily updates")
        data=super(Factor_Multi_Portfolio, self).before_backtest(data)
        self._queue=Queue(maxsize=self.rebalance_window)
        self._periods=0
        self._last_index=data.index[0]
        return data
    
    @staticmethod
    def average_portfolios(queue):
        """Compose multiple portfolios on the queue and returns one vector of weights
        :queue: queue of weights vectors
        """
        return np.mean(list(queue.queue),axis=0)
    
    def update_weights(self, current_index, current_weights, data):
        current_date=data.index[len(data)-1]
        
        it_data = data[data.index >= self._last_index]
        for index, row in it_data.iterrows():
            if(index != current_date):
                if(self._last_index.month != index.month):
                    #there is a portfolio
                    temp_df = it_data.loc[:index]
                    weights = super(Factor_Multi_Portfolio,self).update_weights(index, [], temp_df)
                    self._periods+=1
                    if(self._queue.full()):
                        #dequeue element
                        self._queue.get()
                    self._queue.put(weights)
        
        #current regular rebalance
        weights = super(Factor_Multi_Portfolio,self).update_weights(current_index, current_weights, data)
        self._periods+=1
        if(self._queue.full()):
            #dequeue element
            self._queue.get()
        self._queue.put(weights)
        
        self._last_index=current_index
        
        if(self._queue.full()):
            return self.average_portfolios(self._queue)
        else:
            return [0.]*self.specialists_num