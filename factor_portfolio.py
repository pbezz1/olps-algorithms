'''
Created on Nov 20, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np
import load_factors as lf
import datetime
from algorithm import Algorithm


class Factor_Portfolio(Algorithm):
    
    def __init__(self, assets_list, factor_name, portfolio_size, rebalance_window):
        """Factor portfolio algorithm that calculates the daily returns for a factor based ranked portfolio
        :factor_name: string with factor name
        :assets_list: list of Asset objects
        :portfolio_size: number of assets in the portfolio
        :rebalance_window: period between each rebalance
        """
        super(Factor_Portfolio, self).__init__()
        self.factor_df = lf.create_factor_df(assets_list, factor_name, True)
        self.portfolio_size=portfolio_size
        self.rebalance_window=rebalance_window
        #first portfolio is empty
        self.portfolio=[] 
        self.factor_index=0
        self.next_rebalance_date=None
        self.portfolio_lists=[]
        self.rebalance_dates=[]
        self.factor_used_dates=[]    
        self.df_portfolios=None
        
    def before_backtest(self, data):
        #crop data to match factor df
        data = data[data.date > self.factor_df.date[0]]
        data = data.reset_index(drop=True)
        #first row is time to rebalance
        self.next_rebalance_date=data['date'][self.factor_index]
        
        return data
    
    
    def update_weights(self, current_index, current_weights, data):
        current_date=data['date'][len(data)-1]
        
        if(current_date >= self.next_rebalance_date):    
            while((self.factor_index+1 < len(self.factor_df)) 
                  and (self.next_rebalance_date > self.factor_df['date'][self.factor_index+1])):
                factor_index=self.factor_index+1
            factors=self.factor_df.loc[self.factor_index,self.factor_df.columns[1:len(self.factor_df.columns)]]   
            factors=pd.Series.sort_values(factors,ascending=False) 
            #build portfolio
            self.portfolio=[]
            for i in range(len(factors)):
                if((len(self.portfolio) < self.portfolio_size) and (not np.isnan(factors[i]))):
                    self.portfolio.append(factors.index[i])
            
            self.rebalance_dates.append(current_date)
            self.factor_used_dates.append(self.factor_df.loc[self.factor_index,'date'])
            self.portfolio_lists.append(self.portfolio)
            
            self.next_rebalance_date=self.next_rebalance_date+datetime.timedelta(days=self.rebalance_window)
            
            weights=[]
            if self.portfolio:
                weight=1.0/len(self.portfolio)
                for asset_name in data.columns[1:len(data.columns)]:
                    if asset_name in self.portfolio:
                        weights.append(weight)
                    else:
                        weights.append(0.0)
            return weights 
        else:
            return current_weights
    
    def after_backtest(self):
        self.df_portfolios = pd.DataFrame(columns=['date','factor_date','portfolio'])
        self.df_portfolios['date']=self.rebalance_dates
        self.df_portfolios['portfolio']=self.portfolio_lists
        self.df_portfolios['factor_date']=self.factor_used_dates
    