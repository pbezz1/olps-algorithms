from __future__ import division
import numpy as np
import pandas as pd
from algorithm import Algorithm
from filter import Filter


class Multiplicative_Weights(Algorithm):
    
    def __init__(self, params):
        """Runs the multiplicative weigths algorithm
        :eta: learning rate parameter
        :beta: fixed share parameter. if none is given, the original version of the algorithm is used
        """
        super(Multiplicative_Weights, self).__init__(params)
        
        self._set_default_parameter('eta', 0.01)
        self._set_default_parameter('beta', None)
        
    @property
    def name(self):
        return 'MWU'+str(self.params['eta'])
    
    def add_filter(self, value):
        """Creates filter
        :value: can be a Filter or a path to a file
        """
        if(isinstance(value, Filter)):
            self._filter=value
        elif(isinstance(value, str)):
            self._filter=Filter(file_path=value)
        else:
            raise ValueError("Filter type is not supported")
    
    def multiplicative_weigths_linear_update(self, update_returns, gains_vec, specialists_num):     
        """Linear update rule for multiplicative weigths method
        not in use"""
        for specialist in range(specialists_num):
            gains_vec[specialist] = gains_vec[specialist] * ((1 + self.params['eta']) * (update_returns[specialist]-1))
        
        gains_vec = self.normalize(gains_vec)
        
        return gains_vec
    
    
    def multiplicative_weigths_exp_update(self, update_returns, gains_vec, specialists_num):
        """Exponential update rule for multiplicative weigths method
        """
        for specialist in range(specialists_num):
            gains_vec[specialist] = gains_vec[specialist] * np.exp(self.params['eta'] * (update_returns[specialist]-1))
        
        gains_vec = self.normalize(gains_vec)
    
        return gains_vec
    
    def adaptive_regret_update(self, update_returns, gains_vec, specialists_num):
        """Implements the adaptive regret rule for both static and dynamic beta values
        """
        gains_vec = self.multiplicative_weigths_exp_update(update_returns, gains_vec, specialists_num)
    
        
        for specialist in range(specialists_num):
            gains_vec[specialist] =(self.params['beta']/specialists_num)+((1-self.params['beta'])*gains_vec[specialist])
        
        gains_vec = self.normalize(gains_vec)
    
        return gains_vec
    
    def before_backtest(self, data):
        data = super(Multiplicative_Weights,self).before_backtest(data)
        self.update_data=data
        self._last_index=None
        self.gains_df=[]
        self._last_gains=None
        return data
    
    def update_weights(self,current_index, current_weights, data):        
        
        if(self._last_index is None):
            weights_vec = Algorithm.getUCRP_weights(self.specialists_num)
        else:
            current_result=data[(data.index >= self._last_index) & (data.index < current_index)]
            update_returns=np.prod(current_result+1, axis=0)
            if(self.params['beta'] is None):
                weights_vec = self.multiplicative_weigths_exp_update(update_returns, self._last_gains , self.specialists_num)
            else:
                weights_vec = self.adaptive_regret_update(update_returns, self._last_gains, self.specialists_num)
        
        self._last_gains=weights_vec[:]
        
        self.gains_df.append(self._last_gains)
        
        if(self._filter is not None):
            weights_vec = pd.Series(weights_vec,index=data.columns)
            tradable_assets=list(self._filter.get_tradable_assets(current_index))
            #assets not in filter list should have 0-weight
            weights_vec[~weights_vec.index.isin(tradable_assets)]=0.0
            weights_vec=self.normalize(weights_vec)
            
        self._last_index=current_index  
                
        return weights_vec
    
    def after_backtest(self):
        self.gains_df=pd.DataFrame(self.gains_df)
