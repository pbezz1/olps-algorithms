import pandas as pd
from asset import Asset

#loads all factors files for given assets list
#assets - list of string
#factors - list of string
def loadAssets (assets ,factors):
    assets_list = []
    for asset_name in assets:
        asset = Asset(asset_name)
        for factor_name in factors:
            file_path = "data/"+factor_name+"/"+asset_name+".csv"
            if (os.stat(file_path).st_size != 0):
                data = pd.DataFrame.from_csv(file_path,index_col=None,header=None)
                data.columns = ['date',factor_name]
                asset.add_factor(factor_name, data)
                #print("Adding "+factor_name+" to "+asset_name+" first value is:%d"%data.loc[1,1])
        assets_list.append(asset)
    return assets_list

#Creates an extra factor for each asset based on the ratio of numerator_factor and denominator_factor
#assets - list of Asset
#numer_factor - string
#denom_factor - string
def createExtraFactor(assets, numer_factor, denom_factor, extra_factor_name):
    for asset in assets_list:
        numer_factor_series = asset.get_factor(numer_factor)
        denom_factor_series = asset.get_factor(denom_factor)
        merge = numer_factor_series.merge(denom_factor_series, on='date', how='inner')
        merge[extra_factor_name]=merge[numer_factor]/merge[denom_factor]
        del merge[numer_factor]
        del merge[denom_factor]
        asset.add_factor(extra_factor_name,merge)
    
#initialize factors and assets list
assets = ['ABEV3','BBDC4','PETR4','VALE5']
factors = ['book_value', 'market_value','net_equity','net_income','qty_shares','total_debt','close_unadjusted']

#loads data
assets_list=loadAssets(assets,factors)

#create extra factors
createExtraFactor(assets_list,'close_unadjusted','book_value','price_to_book')