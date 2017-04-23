import multiplicative_weigths as mw
import load_files as lf
import numpy as np
import optimization as opt
import time

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
    print("Example of multiplicative weigths with linear update")
    start = time.time()
    result = mw.multiplicative_weigths(raw_data, 0.3, 1)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' %(totalReturn,(end-start)))

    print("Example of multiplicative weigths with exponential update")
    start = time.time()
    result = mw.multiplicative_weigths(raw_data, 0.3, 2)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

    print("Example of adaptive regret with fixed beta")
    start = time.time()
    beta= 1.00/(len(raw_data.columns)-1) #1/number_of_experts
    result = mw.multiplicative_weigths(raw_data, 0.3, 3,True,beta=beta)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

    print("Example of adaptive regret with varying beta")
    start = time.time()
    beta = np.random.random(raw_data.__len__())
    result = mw.multiplicative_weigths(raw_data, 0.3, 3, True,beta=beta)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

    print("Example of adaptive regret with fixed beta and deterministic prediction")
    start = time.time()
    beta = np.random.random(raw_data.__len__())
    result = mw.multiplicative_weigths(raw_data, 0.3, 3, False,beta=beta)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The total return was %.4f. Took %.4f seconds' % (totalReturn, (end - start)))

    print("Example of eta optimization")
    start = time.time()
    beta= 1.00/(len(raw_data.columns)-1) #1/number_of_experts
    opt_eta = opt.optimizeEta(raw_data, 20, 10, 3, True, beta)
    end = time.time()
    totalReturn=result['Result'].sum()
    print('End of example. The opt eta found was %.2f. Took %.4f seconds' % (opt_eta, (end - start)))
except Exception as error:
        print(repr(error))





