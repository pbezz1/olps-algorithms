import multiplicative_weigths as mw
import numpy as np
import load_factors as lf
import time
import matplotlib


def plot_results(result):
    specialists_num = len(result.columns) - 3
    for specialist in range(1, specialists_num + 1):
        specialist_name = result.columns[specialist]
        cum_col = "Cum_%s" % specialist_name
        result[cum_col] = result[specialist_name].cumsum(axis=0)

    result["Cum_Result"] = result['Result'].cumsum(axis=0)
    
    result.plot(x='date', y=result.columns[specialists_num + 3:2 * specialists_num + 4])

#Example
#initialize factors and assets list
assets = ['ABEV3','BBDC4','PETR4','VALE5']
factors = ['percentage_return']
assets_list=lf.load_assets(assets,factors)
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
    plot_results(result)
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

except Exception as error:
        print(repr(error))