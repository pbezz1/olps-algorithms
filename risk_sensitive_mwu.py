'''
Created on Nov 20, 2017

@author: ckubudi
'''

import multiplicative_weigths as mw
from algorithm import Algorithm
from multiplicative_weigths import Multiplicative_Weights


class Risk_Sensitive_MWU(Multiplicative_Weights):
        
    def __init__(self, eta, period, risk_window, beta=None):
        """
        :risk_window': std rolling window used to risk adjusting
        """
        super(Risk_Sensitive_MWU, self).__init__(eta, period, beta)
        self.risk_window=risk_window
        
    def risk_sensitive(self, raw_data):
        """Function to build risk sensitive data as described on Risk-Sensitive Online Learning" 
        by Eyal Even-Dar, Michael Kearns, and Jennifer Wortman
        :raw_data': dataframe with each column representing a specialist, except for the first one that is the date
        """
        risk_mod_data=raw_data.copy()
        columns = raw_data.columns
        for i in range(1,len(columns)):
            series=risk_mod_data[columns[i]]
            series_stdev=series.rolling(window=self.risk_window,center=False).std()
            series_stdev=series_stdev.fillna(0)
            series_transform=series-series_stdev
            risk_mod_data[columns[i]]=series_transform
        return risk_mod_data
    
    def before_backtest(self, data):
        """to do before backtest
        :data: dataframe with returns and dates
        """
        #update_data: dataframe with the same shape as raw_data, used only to calculate the gains
        self.update_data=self.risk_sensitive(data)
        
        return data
