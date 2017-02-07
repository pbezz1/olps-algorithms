import multiplicative_weigths as mw

print("Hello World!")

test_weigths = [2.5 , 40.77 , 8.23, 5.0, 4.0, 10.00]

maj_mode = mw.decision_mode.Majority
dis_mode = mw.decision_mode.Distributed

print "The max weigth index is " , mw.make_decision(test_weigths, dis_mode)

