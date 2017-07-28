import pandas as pd
import os
import numpy as np
import datetime
from asset import Asset

#loads all factors files for given assets list
#assets - list of string
#factors - list of string
def load_assets (assets ,factors):
    assets_list = []
    for asset_name in assets:
        asset = Asset(asset_name)
        for factor_name in factors:
            file_path = "data/"+factor_name+"/"+asset_name+".csv"
            if (os.stat(file_path).st_size != 0):
                data = pd.DataFrame.from_csv(file_path,index_col=None,header=None)
                data.columns = ['date',factor_name]
                data['date']=pd.to_datetime(data['date'], format='%m/%d/%Y').dt.date
                asset.add_factor(factor_name, data)
                #print("Adding "+factor_name+" to "+asset_name+" first value is:%d"%data.loc[1,1])
        assets_list.append(asset)
    return assets_list

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
def create_factor_df(assets_list, factor_name):
    data = None
    for asset in assets_list:
        factor_series=asset.get_factor(factor_name)
        if(data is None):
            data=factor_series
            data.columns=['date',asset.name]
        else:
            data = data.merge(factor_series, on='date', how='outer')
            data.rename(columns={data.columns[len(data.columns)-1]:asset.name}, inplace=True)
        
    return data


#Calculate the daily returns for a factor based ranked portfolio
#'assets list': list of Asset 
#'factor name': string with factor name
#'portfolio size': number of assets in the portfolio
#'rebalance_window': period between each rebalance
def create_factor_portfolio(assets_list, factor_name, portfolio_size, rebalance_window):
    data = create_factor_df(assets_list,factor_name)
    returns = create_factor_df(assets_list,'percentage_return')
    returns = returns.dropna(how='any')
    portfolio_returns=[]
    portfolio_lists=[]
    rebalance_dates=[]
    factor_used_dates=[]
    assets_number=len(assets_list)
    
    #first portfolio is empty
    portfolio=[]
    factor_index=0
    next_rebalance_date=returns['date'][factor_index]+datetime.timedelta(days=rebalance_window)
    
    count=0
    for index, row in returns.iterrows():       
        while(row['date'] >= next_rebalance_date):    
            while((factor_index+1 < len(data)) and (next_rebalance_date > data['date'][factor_index+1])):
                factor_index=factor_index+1
            #to do - check if last factor date is recent enough
            factors=data.loc[factor_index,data.columns[1:len(data.columns)]]   
            factors=pd.Series.sort_values(factors,ascending=False) 
            #build portfolio
            portfolio=[]
            for i in range(len(factors)):
                if((len(portfolio) < portfolio_size) and (not np.isnan(factors[i]))):
                   portfolio.append(factors.index[i])
            
            rebalance_dates.append(row['date'])
            factor_used_dates.append(data.loc[factor_index,'date'])
            portfolio_lists.append(portfolio)
            
            next_rebalance_date=next_rebalance_date+datetime.timedelta(days=rebalance_window)
        
        p_return=0.0
        if(portfolio):
            for asset_name in portfolio:
                p_return=p_return+row[asset_name]
            p_return=p_return/len(portfolio)

        #set p_return
        portfolio_returns.append(p_return)
        
    
    df = pd.DataFrame(columns=['date','return'])
    df['date']=returns['date']
    df['return']=portfolio_returns
    
    df_portfolios = pd.DataFrame(columns=['date','factor_date','portfolio'])
    df_portfolios['date']=rebalance_dates
    df_portfolios['portfolio']=portfolio_lists
    df_portfolios['factor_date']=factor_used_dates
    
    return df,df_portfolios
    
#initialize factors and assets list
assets = ['ABEV3','BBDC4','PETR4','VALE5']
factors = ['book_value', 'market_value','net_equity','net_income','qty_shares'
           ,'total_debt','close_unadjusted','percentage_return']

#loads data in array of Asset object
assets_list=load_assets(assets,factors)

#create extra factors
create_extra_factor(assets_list, 'close_unadjusted','book_value','price_to_book') 

#create portfolio returns
ptobook,ptobook_portfolios = create_factor_portfolio(assets_list,'price_to_book',3,91)