'''
Created on Jan 17, 2018

@author: ckubudi
'''
import os
import numpy as np
import pandas as pd


class Profit_Stop_Matcher():

    def __init__(self, profit, stop, hedge_asset_column):
        #returns.columns.get_loc('IBOV')
        self.profit=profit
        self.stop=stop
        self.hedge_asset_column=hedge_asset_column
        self.current_high=None
        
    def reset_trailing(self):
        self.current_high=None
        
    def new_return(self, weights_arr, returns_arr):
        """For each return row, receives current weights array and compound individual returns array and process the profit/stop
        returns the new weights array
        :weights_arr :  array of weights
        :returns_arr : array of returns
        """
        if(self.current_high is None):
            self.current_high = np.repeat(1.0,len(returns_arr))
        
        #get returns relative to hedge
        returns_arr=np.copy(returns_arr)
        returns_arr=returns_arr / returns_arr[self.hedge_asset_column]
        
        #test stop
        #get current maximum drawdown for each asset
        self.current_high=np.maximum(self.current_high,returns_arr)
        drawdown_arr=1-returns_arr/self.current_high
        drawdown_arr=np.around(drawdown_arr,decimals=4)
        #get total position on stopped assets and set it to hedge asset
        stop_mask=(drawdown_arr>=self.stop)
        stopped_total_weight = np.sum(weights_arr[stop_mask])
        weights_arr[stop_mask] = 0.0
        weights_arr[self.hedge_asset_column]+=stopped_total_weight
        
        #test profit
        profit_mask=(returns_arr>=(1+self.profit))
        profited_total_weight=np.sum(weights_arr[profit_mask])
        weights_arr[profit_mask]=0.0
        weights_arr[self.hedge_asset_column]+=profited_total_weight
        
        return weights_arr