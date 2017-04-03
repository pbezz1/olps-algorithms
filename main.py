import multiplicative_weigths as mw
import load_files as lf
import matplotlib

#matplotlib.style.use('ggplot')

#Example
result = lf.build_data('data/')
result = mw.multiplicative_weigths(result, 0.3, 2)

specialists_num = len(result.columns) - 3
for specialist in range(1, specialists_num + 1):
    specialist_name = result.columns[specialist]
    cum_col= "Cum_%s" % specialist_name
    result[cum_col] = result[specialist_name].cumsum(axis=0)

result["Cum_Result"] = result['Result'].cumsum(axis=0)

result.plot(x='date', y=result.columns[specialists_num+3:2*specialists_num+4])