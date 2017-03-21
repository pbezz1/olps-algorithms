import multiplicative_weigths as mw
import load_files as lf
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

print("Hello World!")

result = lf.build_data('data/')
result = mw.multiplicative_weigths(result, 0.5)

specialists_num = len(result.columns) - 3
for specialist in range(1, specialists_num + 1):
    specialist_name = result.columns[specialist]
    cum_col= "Cum_%s" % specialist_name
    result[cum_col] = result[specialist_name].cumsum(axis=0)

result["Cum_Result"] = result['Result'].cumsum(axis=0)

result.plot(x='date', y=result.columns[specialists_num+3:2*specialists_num+4])

test_weigths = [2.5 , 40.77 , 8.23, 5.0, 4.0, 10.00]

print "The max weigth index is " , mw.make_decision(test_weigths, dis_mode)


