'''
Created on Nov 20, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np
import load_factors as lf
import datetime
from algorithm import Algorithm
from filter import Filter

class Factor_Portfolio(Algorithm):
    
    def __init__(self, assets_list, factor_name, portfolio_size):
        """Factor portfolio algorithm that calculates the daily returns for a factor based ranked portfolio
        :factor_name: string with factor name
        :assets_list: list of Asset objects
        :portfolio_size: number of assets in the portfolio
        """
        super(Factor_Portfolio, self).__init__()
        if assets_list:
            self.factor_df = lf.create_factor_df(assets_list, factor_name, True)
        self.portfolio_size=portfolio_size
        self._factor_name=factor_name
    
    @property
    def name(self):
        return "Factor "+self._factor_name
    
    def reset_params(self):
        self.portfolio=[] 
        self.factor_idx=0
        self.portfolio_lists=[]
        self.rebalance_dates=[]
        self.factor_used_dates=[]    
        self.df_portfolios=None

        
    def add_filter(self, value):
        self._filter=Filter(file_path=value)
    
    
    def isWhiteListed(self, asset, date):
        if(self._filter is not None):
            return self._filter.isWhiteListed(asset, date)
        else:
            return True    
        
    def before_backtest(self, data):
        data=super(Factor_Portfolio,self).before_backtest(data)
        #reset params
        self.reset_params()
        #crop data to match factor df
        data = data[data.index > self.factor_df.index[0]]
        return data
    
    
    def update_weights(self, current_index, current_weights, data):
        current_date=data.index[len(data)-1]
        
        while((self.factor_idx+1 < len(self.factor_df)) 
              and (current_date > self.factor_df.index[self.factor_idx+1])):
            self.factor_idx=self.factor_idx+1

        #sort assets by factor
        factors=self.factor_df.iloc[self.factor_idx,:]   
        factors=pd.Series.sort_values(factors,ascending=False) 
        
        #build portfolio
        self.portfolio=[]
        for i in range(len(factors)):
            if((len(self.portfolio) < self.portfolio_size) and (not np.isnan(factors[i]))):
                asset=factors.index[i]
                if(self.isWhiteListed(asset, self.factor_df.index[self.factor_idx])):
                    self.portfolio.append(asset)
        
        self.rebalance_dates.append(current_date)
        self.factor_used_dates.append(self.factor_df.index[self.factor_idx])
        self.portfolio_lists.append(self.portfolio)
        
        #build weights vec
        weights=[]
        if self.portfolio:
            weight=1.0/len(self.portfolio)
            for asset_name in data.columns:
                if asset_name in self.portfolio:
                    weights.append(weight)
                else:
                    weights.append(0.0)
        else:
            weights = [0.0] * self.specialists_num
            
        return weights
    
    def after_backtest(self):
        #build dataframe with portfolios
        self.df_portfolios = pd.DataFrame(columns=['factor_date','portfolio'],index=self.rebalance_dates)
        self.df_portfolios['factor_date']=self.factor_used_dates
        self.df_portfolios['portfolio']=self.portfolio_lists
    