'''
Created on Feb 15, 2018

@author: ckubudi
'''
import pandas as pd
import numpy as np
from algorithm import Algorithm
from filter import Filter
from random import shuffle


class Shuffle_Portfolio(Algorithm):

    def __init__(self):
        """Factor portfolio algorithm that calculates the daily returns for a factor based ranked portfolio
        :portfolio_size: number of assets in the portfolio
        :args: list of dataframes. each one is representing one factor. minimum of one, otherwise there is no factor.
        """
        super(Shuffle_Portfolio, self).__init__()
        
        ## PARAMS 
        #set default params
        self.portfolio_size=15
        self.reverse_order=False
        self.factor_filter=None
        self.pos_sizer='uniform'
        
    @property
    def name(self):
        return "Shuffle Portfolio"
    
    def reset_state(self):
        self.portfolio=[] 
        self.portfolio_lists=[]
        self.rebalance_dates=[]
    
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
        
    def is_white_listed(self, asset, date):
        if(self._filter is not None):
            return self._filter.is_white_listed(asset, date)
        else:
            return True    
        
    def before_backtest(self, data):
        data=super(Shuffle_Portfolio,self).before_backtest(data)
        #reset params
        self.reset_state()
        
        return data
    
    @staticmethod
    def uniform_pos_sizer(portfolio, assets_list):
        specialist_num=len(assets_list)
        weights=[]
        if portfolio:
            weight=1.0/len(portfolio)
            for asset_name in assets_list:
                if asset_name in portfolio:
                    weights.append(weight)
                else:
                    weights.append(0.0)
        else:
            weights = [0.0] * specialist_num
        
        return weights
        
    def update_weights(self, current_index, current_weights, data):
        shuffle_list=list(data.columns)
        shuffle(shuffle_list)
        
        #build portfolio
        self.portfolio=[]
        for i in range(len(shuffle_list)):
            if((len(self.portfolio) < self.portfolio_size)):
                asset=shuffle_list[i]
                if(self.is_white_listed(asset, current_index)):
                    self.portfolio.append(asset)
        
        self.rebalance_dates.append(current_index)
        self.portfolio_lists.append(self.portfolio)
        
        weights=self.uniform_pos_sizer(self.portfolio, data.columns)
        
        return weights
    
    def after_backtest(self):
        #build dataframe with portfolios
        self.df_portfolios = pd.DataFrame(columns=['portfolio'],index=self.rebalance_dates)
        self.df_portfolios['portfolio']=self.portfolio_lists
    