'''
Created on Nov 19, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np
import scipy.optimize as optimize
import logging
from algorithm import Algorithm

class Pattern_Matching(Algorithm):
    

    def __init__(self, window_size, c_threshold):
        super(Pattern_Matching, self).__init__()
        self.window_size=window_size
        self.c_threshold=c_threshold

    @staticmethod
    def process_similar_windows(current_window, historical_df, window_size, c_threshold):
        """ Searches given historical dataframe for similar price windows and returns the next step for each of them
        :current_window: current past window as list of array
        :historical df: dataframe with returns for each asset
        :window_size: size of the window to search
        :c_threshold: minimum correlation to recognize similar patterns
        """
        
        historical_list = historical_df.values.flatten()
        current_window=np.asarray(current_window)
        similar_next_steps = []
    
        experts_num = len(historical_df.columns)  
        values_window=experts_num*window_size
        it_window_start=0
        it_window_end=values_window
        
        while(it_window_end <= len(historical_list)-experts_num):
            it_window = historical_list[it_window_start:it_window_end]
            
            if(np.corrcoef(current_window, it_window)[0,1] >= c_threshold):
                next_step=historical_list[it_window_end:it_window_end+experts_num]
                similar_next_steps.append(next_step)
            
            it_window_start+=experts_num
            it_window_end+=experts_num
        
        return similar_next_steps
    
    
    @staticmethod
    def get_bcrp(X, metric='return', max_leverage=1, rf_rate=0., alpha=0., freq=252, no_cash=False, sd_factor=1., **kwargs):
        """ Find best constant rebalanced portfolio with regards to some metric.
        :param X: Prices in ratios.
        :param metric: what performance metric to optimize, can be either `return` or `sharpe`
        :max_leverage: maximum leverage
        :rf_rate: risk-free rate for `sharpe`, can be used to make it more aggressive
        :alpha: regularization parameter for volatility in sharpe
        :freq: frequency for sharpe (default 252 for daily data)
        :no_cash: if True, we can't keep cash (that is sum of weights == max_leverage)
        """
        assert metric in ('return', 'sharpe', 'drawdown')
    
        x_0 = max_leverage * np.ones(X.shape[1]) / float(X.shape[1])
        objective = lambda b: -np.sum(np.log(np.maximum(np.dot(X - 1, b) + 1, 0.0001)))
        
        if no_cash:
            cons = ({'type': 'eq', 'fun': lambda b: max_leverage - sum(b)},)
        else:
            cons = ({'type': 'ineq', 'fun': lambda b: max_leverage - sum(b)},)
    
        while True:
            # problem optimization
            res = optimize.minimize(objective, x_0, bounds=[(0., max_leverage)]*len(x_0), constraints=cons, method='slsqp', **kwargs)
    
            # result can be out-of-bounds -> try it again
            EPS = 1E-7
            if (res.x < 0. - EPS).any() or (res.x > max_leverage + EPS).any():
                X = X + np.random.randn(1)[0] * 1E-5
                logging.debug('Optimal weights not found, trying again...')
                continue
            elif res.success:
                break
            else:
                if np.isnan(res.x).any():
                    logging.warning('Solution does not exist, use zero weights.')
                    res.x = np.zeros(X.shape[1])
                else:
                    logging.warning('Converged, but not successfully.')
                break
    
        return res.x
        
    
    def update_weights(self, current_index, current_weights, data):
        data_len=len(data)
        current_window = data.iloc[data_len-self.window_size:data_len,:].values.flatten()
        
        next_steps = self.process_similar_windows(current_window, data, self.window_size, self.c_threshold)
        
        if not next_steps:
            weights = self.getUCRP_weights(self.specialists_num)
        else:    
            next_steps = pd.DataFrame(next_steps)
            weights = self.get_bcrp(next_steps)
        
        return weights
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


