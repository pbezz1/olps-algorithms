import multiplicative_weigths as mw
import load_files as lf

print("Hello World!")

result = lf.build_data('data/')

mw.multiplicative_weigths(result, 0.5)

test_weigths = [2.5 , 40.77 , 8.23, 5.0, 4.0, 10.00]

print "The max weigth index is " , mw.make_decision(test_weigths, dis_mode)


