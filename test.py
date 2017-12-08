'''
Created on Dec 4, 2017

@author: ckubudi
'''

import pickle
import load_factors as lf
import time
from asset import Asset
from factor_portfolio import Factor_Portfolio
from factor_multi_portfolio import Factor_Multi_Portfolio
from multiplicative_weigths import Multiplicative_Weights
from Cython.Shadow import returns

#load objects
assets_list=pickle.load(open('../dump/assets_list.p','rb'))
returns=pickle.load(open('../dump/returns.p', 'rb'))
#get only PN assets
assets_list=lf.get_only_PN(assets_list)

start = time.time()
algorithm = Multiplicative_Weights(eta=0.3)
result = algorithm.run(returns,start_date='01/01/2006')
end = time.time()
print('MWU Elapsed time: ', (end-start), ' segundos')

"""
start = time.time()
algorithm = Factor_Portfolio(assets_list, 'momentum', 15)
algorithm.add_filter('../data/filter/IBX.csv')
algorithm.portfolio_size=15
algorithm.rebalance_window=1
algorithm.rebalance_period='monthly'
result = algorithm.run(returns,start_date='01/01/2006')
end = time.time()
print('Factor Portfolio Elapsed time: ', (end-start), ' segundos')
"""
"""
start = time.time()
algorithm = Factor_Multi_Portfolio(assets_list, 'momentum', 15, n_portfolios=12)
algorithm.add_filter('../data/filter/IBX.csv')
end = time.time()
print('Factor Multi Portfolio creation time: ', (end-start), ' segundos')

start = time.time()
algorithm.portfolio_size=15
algorithm.rebalance_window=1
algorithm.rebalance_period='monthly'
result = algorithm.run(returns,start_date='01/01/2006')
end = time.time()
print('Factor Multi Portfolio 1 run time: ', (end-start), ' segundos')
print(result.summary())

start = time.time()
algorithm.portfolio_size=15
algorithm.rebalance_window=6
algorithm.rebalance_period='monthly'
result = algorithm.run(returns,start_date='01/01/2006')
end = time.time()
print('Factor Multi Portfolio 6 run time: ', (end-start), ' segundos')
print(result.summary())
"""


print('end')