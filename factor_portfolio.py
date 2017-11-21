'''
Created on Nov 20, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np
import load_factors as lf
import datetime


#Calculate the daily returns for a factor based ranked portfolio
#'factor_df': dataframe with factors for each asset
#'return': dataframe with retuns for each asset
#'portfolio size': number of assets in the portfolio
#'rebalance_window': period between each rebalance
def create_factor_portfolio(factor_df, returns, portfolio_size, rebalance_window):
    portfolio_lists=[]
    rebalance_dates=[]
    factor_used_dates=[]
    #assets_number=len(assets_list)
    
    #crop returns to match first factor date
    returns = returns[returns.date > factor_df.date[0]]
    returns = returns.reset_index(drop=True)
    
    #first portfolio is empty
    portfolio=[]
    factor_index=0
    next_rebalance_date=returns['date'][factor_index]
    
    portfolio_dates=[]
    portfolio_returns=[]
    
    for index, row in returns.iterrows():  
        while(row['date'] >= next_rebalance_date):    
            while((factor_index+1 < len(factor_df)) and (next_rebalance_date > factor_df['date'][factor_index+1])):
                factor_index=factor_index+1
            factors=factor_df.loc[factor_index,factor_df.columns[1:len(factor_df.columns)]]   
            factors=pd.Series.sort_values(factors,ascending=False) 
            #build portfolio
            portfolio=[]
            for i in range(len(factors)):
                if((len(portfolio) < portfolio_size) and (not np.isnan(factors[i]))):
                    portfolio.append(factors.index[i])
            
            rebalance_dates.append(row['date'])
            factor_used_dates.append(factor_df.loc[factor_index,'date'])
            portfolio_lists.append(portfolio)
            
            next_rebalance_date=next_rebalance_date+datetime.timedelta(days=rebalance_window)
        
        p_return=0.0
        if(portfolio):
            for asset_name in portfolio:
                asset_return=row[asset_name]
                if(not np.isnan(asset_return)):
                    p_return=p_return+asset_return
            p_return=p_return/len(portfolio)

        #set p_return
        portfolio_dates.append(row['date'])
        portfolio_returns.append(p_return)
        
    
    df = pd.DataFrame(columns=['date','return'])
    df['date']=portfolio_dates
    df['return']=portfolio_returns
    
    df_portfolios = pd.DataFrame(columns=['date','factor_date','portfolio'])
    df_portfolios['date']=rebalance_dates
    df_portfolios['portfolio']=portfolio_lists
    df_portfolios['factor_date']=factor_used_dates
    
    return df,df_portfolios

def run(data, assets_list, factor_name, portfolio_size, rebalance_window):
    factor_df = lf.create_factor_df(assets_list, factor_name, True)
    return create_factor_portfolio(factor_df, data, portfolio_size, rebalance_window)
    