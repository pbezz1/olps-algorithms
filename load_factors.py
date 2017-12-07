import pandas as pd
import os
import numpy as np
import datetime
from asset import Asset

#add factor to asset
def add_factor(asset, file_path, factor_name):
    if (os.stat(file_path).st_size != 0):
        data = pd.DataFrame.from_csv(file_path,header=None)
        data.index.name='date'
        data.columns = [factor_name]
        #data.index=pd.to_datetime(data.index, format='%Y-%m-%d').dt.date
        asset.add_factor(factor_name, data)


def load_assets (factors, data_path):
    """loads all factors files for all files that have close prices
    factors - list of string
    """
    assets_dict={}
    asset = None
    #load close prices
    for file in os.listdir(data_path+'close'):
        if(file.endswith('.csv')):
            file_path = os.path.join(data_path+'close', file)
            file_name=os.path.splitext(file)[0]
            if((os.stat(file_path).st_size != 0)):
                asset=Asset(file_name)
                assets_dict[file_name]=asset
                add_factor(asset, file_path, 'close')
    
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

def create_extra_factor(assets_list, numer_factor, denom_factor, extra_factor_name):
    """Creates an extra factor for each asset based on the ratio of numerator_factor and denominator_factor
    :assets - list of Asset
    :numer_factor - string with factor name
    :denom_factor - string with factor name
    """
    for asset in assets_list:
        numer_factor_series = asset.get_factor(numer_factor)
        denom_factor_series = asset.get_factor(denom_factor)
        join = numer_factor_series.join(denom_factor_series, how='inner')
        join[extra_factor_name]=join[numer_factor]/join[denom_factor]
        del join[numer_factor]
        del join[denom_factor]
        asset.add_factor(extra_factor_name,join)

def create_momentum_factor(assets_list, short_window, long_window, factor_name):
    """ Creates momentum factor
    :assets_list Asset list
    :short_window int represeting the short price to be used
    :long_window int represeting the long price to be used
    :factor_name factor string name
    """
    for asset in assets_list:
        prices = asset.get_factor('close')
        numer_factor = prices.rolling(window=short_window).mean()
        denom_factor = prices.rolling(window=long_window).mean()
        factor=numer_factor/denom_factor
        factor.columns=[factor_name]
        factor=factor[np.isfinite(factor[factor_name])]
        asset.add_factor(factor_name, factor)
 

def create_factor_df(assets_list, factor_name, isForwardFill):
    '''Creates a dataframe with the factors from all assets in 'assets_list'
    :assets_list: list of Asset 
    :factor_name: string with factor name
    '''
    data = None
    for asset in assets_list:
        factor_series=asset.get_factor(factor_name)
        if(factor_series is not None):
            if(data is None):
                data=factor_series
                data.columns=[asset.name]
            else:
                data = data.join(factor_series, how='outer')
                data.rename(columns={data.columns[len(data.columns)-1]:asset.name}, inplace=True)
    
    if(data is not None):
        data.sort_index(inplace=True)
        data = data.dropna(how='all')
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
                    
                    
def _convert_prices(S, replace_missing=True):
    """ Convert prices to returns
    """
    # be careful about NaN values
    X = S / S.shift(1).fillna(method='ffill')
    for name, s in X.iteritems():
        X[name].iloc[s.index.get_loc(s.first_valid_index()) - 1] = 1.

    if replace_missing:
        X = X.fillna(1.)
    
    X = X-1
    if(len(X.columns)==1):    
        X.columns=['return']
    return X

def custom_key(asset):
    return asset.name

def print_list(assets_list):
    for asset in assets_list:
        print(asset.name)

def is_same_company(asset1,asset2):
    """Compare two asset names and returns True in case they are the same company
    """
    asset1_alias=asset1[0:len(asset1)-1]
    asset2_alias=asset2[0:len(asset2)-1]
    if asset1_alias == asset2_alias :
        return True
    else:
        return False
        
def get_only_PN(assets_list):
    if not assets_list:
        return []
    assets_list.sort(key=custom_key,reverse=True)
    new_list=[]
    new_list.append(assets_list[0])
    for idx in range(1,len(assets_list)):
        asset1 = assets_list[idx-1]
        asset2 = assets_list[idx]
        if not is_same_company(asset1.name, asset2.name):
            new_list.append(asset2)
    return new_list
