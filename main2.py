%matplotlib inline
import multiplicative_weigths as mw
import load_files as lf
import numpy as np
import optimization as opt
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
raw_data = lf.build_data('data/')

#runs the algorithm
try:
    start = time.time()
    beta = np.random.random(raw_data.__len__())
    risk_sensivite_data = mw.risk_sensivite(raw_data,30)
    result = mw.multiplicative_weigths(raw_data, 0.3, 2, 90, risk_sensivite_data)
    #result = mw.multiplicative_weigths(raw_data, 0.3, 2, 90, raw_data)
    end = time.time()
    plot_results(result)
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

except Exception as error:
        print(repr(error))