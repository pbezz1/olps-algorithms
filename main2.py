import multiplicative_weigths as mw
import numpy as np
import load_factors as lf
import time
import plot

#Example
#initialize factors and assets list
factors = ['percentage_return']
assets_list=lf.load_assets(factors)
raw_data=lf.create_factor_df(assets_list=assets_list,factor_name='percentage_return')
raw_data=raw_data.dropna(how='any')

#runs the algorithm
try:
    start = time.time()
    beta = np.random.random(raw_data.__len__())
    risk_sensitive_data = mw.risk_sensitive(raw_data,30)
    result = mw.multiplicative_weigths(raw_data, 0.3, 90, risk_sensitive_data)  
    #result = mw.multiplicative_weigths(raw_data, 0.3, 90, raw_data)  
    end = time.time()
    plot.plot_results(result)
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

except Exception as error:
        print(repr(error))