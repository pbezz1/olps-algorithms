'''
Created on Dec 8, 2017

@author: ckubudi
'''
                    
def prices_to_returns(prices, replace_missing=True):
    """ Convert prices dataframe to returns
    :prices: dataframe with prices
    """
    # be careful about NaN values
    X = prices / prices.shift(1).fillna(method='ffill')
    for name, s in X.iteritems():
        X[name].iloc[s.index.get_loc(s.first_valid_index()) - 1] = 1.

    if replace_missing:
        X = X.fillna(1.)
    
    X = X-1
    if(len(X.columns)==1):    
        X.columns=['return']
    return X

def momentum_sma(prices, short_window, long_window):
    """ Creates momentum sma factor
    :prices dataframe with prices
    :short_window int represeting the short price to be used
    :long_window int represeting the long price to be used
    """
    numer_factor = prices.rolling(window=short_window).mean()
    denom_factor = prices.rolling(window=long_window).mean()
    factor=numer_factor/denom_factor
    factor.dropna(how='all',inplace=True)
    return factor

def momentum(prices, short_window, long_window):
    """ Creates classic momentum factor
    :prices dataframe with prices
    :short_window int represeting the short price to be used
    :long_window int represeting the long price to be used
    """
    numer_factor= prices.shift(periods=short_window)
    denom_factor= prices.shift(periods=long_window)
    factor=numer_factor/denom_factor
    factor.dropna(how='all',inplace=True)
    return factor

def vol(returns, window):
    """ Creates vol factor as measured by stdev of returns
    :prices dataframe with price
    :window volatility window size
    """
    factor = returns.rolling(window=window).std()
    factor.dropna(how='all', inplace=True)
    return factor
    
    
    