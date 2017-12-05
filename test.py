'''
Created on Dec 4, 2017

@author: ckubudi
'''

import load_factors as lf
from factor_portfolio import Factor_Portfolio

assets_list=lf.load_assets([], '../data/')
prices=lf.create_factor_df(assets_list,'close',False)
returns=lf._convert_prices(prices)
lf.create_momentum_factor(assets_list, 21, 252, 'momentum')

algorithm = Factor_Portfolio(assets_list, 'momentum', 15)
algorithm.rebalance_window=1
algorithm.rebalance_period='monthly'
algorithm.add_filter('../data/filter/IBX.csv')

result = algorithm.run(returns)
portfolios = algorithm.df_portfolios

result.to_csv('../result.csv')
portfolios.to_csv('../portfolios.csv')


print('end')