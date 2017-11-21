'''
Created on Nov 20, 2017

@author: ckubudi
'''

import multiplicative_weigths as mw


#Function to build risk sensitive data as described on 
#"Risk-Sensitive Online Learning" by Eyal Even-Dar, Michael Kearns, and Jennifer Wortman
#'raw_data': dataframe with each column representing a specialist, except for the first one that is the date
#'window': std rolling window used to risk adjusting
def risk_sensitive(raw_data,window):
    risk_mod_data=raw_data.copy()
    columns = raw_data.columns
    for i in range(1,len(columns)):
        series=risk_mod_data[columns[i]]
        series_stdev=series.rolling(window=window,center=False).std()
        series_stdev=series_stdev.fillna(0)
        series_transform=series-series_stdev
        risk_mod_data[columns[i]]=series_transform
    return risk_mod_data

def run (data, eta, period, risk_window, beta=None):
    risk_sensitive_data=risk_sensitive(data, risk_window)
    return mw.multiplicative_weights(data, eta, period, risk_sensitive_data, beta)
