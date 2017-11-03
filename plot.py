'''
Created on Nov 3, 2017

@author: ckubudi
'''

def plot_results(result):
    specialists_num = len(result.columns) - 3
    for specialist in range(1, specialists_num + 1):
        specialist_name = result.columns[specialist]
        cum_col = "Cum_%s" % specialist_name
        result[cum_col] = result[specialist_name].cumsum(axis=0)

    result["Cum_Result"] = result['Result'].cumsum(axis=0)
    
    result.plot(x='date', y=result.columns[specialists_num + 3:2 * specialists_num + 4])
    
    

def plot_cumulative_returns(data):
     data['cumulative result'] = data['result'].cumsum(axis=0)
     data.plot(x='date', y='cumulative_result')