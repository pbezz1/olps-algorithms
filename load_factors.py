import pandas as pd
import os
import numpy as np
import datetime
from asset import Asset

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

def create_returns(data_path):
    ''' Create returns from prices
    :data_path: path to folder with folder factors
    '''
    for file in os.listdir(data_path+'close'):
        if(file.endswith('.csv')):
            file_path = os.path.join(data_path+'close', file)
            file_name=os.path.splitext(file)[0]
            print(file_name+" is being processed")
            if((os.stat(file_path).st_size != 0)):
                data = pd.DataFrame.from_csv(file_path,index_col=None,header='infer')
                if(len(data.columns) ==  2):
                    data.columns = ['date','close']
                    data['date']=pd.to_datetime(data['date'], format='%m/%d/%Y').dt.date
                    data['return']=data['close']/data['close'].shift(1) - 1
                    data = data.drop([0])
                    del data['close']
                    data.to_csv(os.path.join(data_path+'return')+"/"+file_name+".csv",sep=',',index=False)
                else:
                    print("Something is wrong with data")
        
