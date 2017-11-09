import pandas as pd
import os
import numpy as np
import datetime
from asset import Asset
from pandas.tests.io.parser import skiprows

#add factor to asset
def add_factor(asset, file_path, factor_name):
    if (os.stat(file_path).st_size != 0):
        data = pd.DataFrame.from_csv(file_path,index_col=None,header='infer')
        data.columns = ['date',factor_name]
        data['date']=pd.to_datetime(data['date'], format='%Y-%m-%d').dt.date
        asset.add_factor(factor_name, data)

#loads all factors files for all files that have returns
#factors - list of string
def load_assets (factors, data_path):
    assets_dict={}
    asset = None
    #load returns
    for file in os.listdir(data_path+'return'):
        if(file.endswith('.csv')):
            file_path = os.path.join(data_path+'return', file)
            file_name=os.path.splitext(file)[0]
            if((os.stat(file_path).st_size != 0)):
                asset=Asset(file_name)
                assets_dict[file_name]=asset
                add_factor(asset, file_path, 'return')
    
    #load factors from factors list
    for factor_name in factors:
        for file in os.listdir(data_path+factor_name):
            if(file.endswith('.csv')):
                file_path = os.path.join(data_path+factor_name, file)
                file_name=os.path.splitext(file)[0]
                if(file_name in assets_dict):
                    asset=assets_dict[file_name]
                    add_factor(asset, file_path, factor_name)
                    
    return list(assets_dict.values())

#Creates an extra factor for each asset based on the ratio of numerator_factor and denominator_factor
#assets - list of Asset
#numer_factor - string with factor name
#denom_factor - string with factor name
def create_extra_factor(assets_list, numer_factor, denom_factor, extra_factor_name):
    for asset in assets_list:
        numer_factor_series = asset.get_factor(numer_factor)
        denom_factor_series = asset.get_factor(denom_factor)
        merge = numer_factor_series.merge(denom_factor_series, on='date', how='inner')
        merge[extra_factor_name]=merge[numer_factor]/merge[denom_factor]
        del merge[numer_factor]
        del merge[denom_factor]
        asset.add_factor(extra_factor_name,merge)

        
#Creates a dataframe with the factors from all assets in 'assets_list'
#'assets list': list of Asset 
#'factor name': string with factor name
def create_factor_df(assets_list, factor_name, isForwardFill):
    data = None
    for asset in assets_list:
        factor_series=asset.get_factor(factor_name)
        if(factor_series is not None):
            if(data is None):
                data=factor_series
                data.columns=['date',asset.name]
            else:
                data = data.merge(factor_series, on='date', how='outer')
                data.rename(columns={data.columns[len(data.columns)-1]:asset.name}, inplace=True)
    
    if(data is not None):
        data=data.sort_values(by=['date'])
        data = data.reset_index(drop=True)
        if(isForwardFill):
            data = data.fillna(method='ffill', limit=252) #forward propagation of factors, with 252 as limit


    return data


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