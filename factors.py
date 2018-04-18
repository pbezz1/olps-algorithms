'''
Created on Dec 8, 2017

@author: ckubudi
'''

class Factor():
    
    def __init__(self, source_df, factor_params):
        """
        :source_df: dataframe with data to use for calculating factors
        :factor_params: factor params. may include name, window, etc.
        :*args: optional parameters for factor calculation
        """
        self.source_df=source_df
        self.factor_params=factor_params
    
    def get_factor_df(self):
        factor_name=self.factor_params['factor_name']
        if(factor_name == 'return'):
            if('replace_missing' in self.factor_params):
                return self.prices_to_returns(self.source_df, self.factor_params['replace_missing'])
            else:
                raise ValueError('Invalid parameters for return factor')
        elif(factor_name == 'momentum'):
            if('short_window' in self.factor_params
               and 'long_window' in self.factor_params):
                return self.momentum(self.source_df, self.factor_params['short_window'], self.factor_params['long_window'])
            else:
                raise ValueError('Invalid parameters for momentum factor')
        elif(factor_name == 'momentum_sma'):
            if('short_window' in self.factor_params
               and 'long_window' in self.factor_params):
                return self.momentum_sma(self.source_df, self.factor_params['short_window'], self.factor_params['long_window'])
            else:
                raise ValueError('Invalid parameters for momentum factor')
        elif(factor_name == 'vol'):
            if('window' in self.factor_params):
                return self.vol(self.source_df,self.factor_params['window'])
            else:
                raise ValueError('Invalid parameters for momentum factor')
        else:
            raise ValueError('factor name is not implemented')         
           
    @staticmethod                    
    def prices_to_returns(prices, replace_missing=False):
        """ Convert prices dataframe to returns
        :prices: dataframe with prices
        """
        # be careful about NaN values
        X = prices / prices.shift(1)
        #for name, s in X.iteritems():
        #    X[name].iloc[s.index.get_loc(s.first_valid_index()) - 1] = 1.
    
        if replace_missing:
            X = X.fillna(1.)
        
        X = X-1
        if(len(X.columns)==1):    
            X.columns=['return']
        X.name='return'
        return X
    
    @staticmethod
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
        factor.name='momentum_sma'+str(short_window)+'x'+str(long_window)
        return factor
    
    @staticmethod                    
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
        factor.name='momentum'+str(short_window)+'x'+str(long_window)
        return factor
    
    @staticmethod                    
    def vol(returns, window):
        """ Creates vol factor as measured by stdev of returns
        :prices dataframe with price
        :window volatility window size
        """
        factor = returns.rolling(window=window).std()
        factor.dropna(how='all', inplace=True)
        factor.name='vol'+str(window)
        return factor
        
        
        