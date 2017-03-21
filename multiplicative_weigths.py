from __future__ import division
import numpy as np

#Makes decision based on distribution criteria given by weigths_list
def make_distributed_decision (weigths_list):
    #calculate weigths sum
    weigths_sum=0
    for weigth in weigths_list:
        weigths_sum+=weigth

    #calculate probabilities
    probabilities_list = []
    for weigth in weigths_list:
        probabilities_list.append(weigth/weigths_sum)

    #sample and choose
    indexes = np.arange(0, len(weigths_list))
    index = np.random.choice(indexes , p=probabilities_list )
    return index

#Runs the multiplicative weigths algorithm based on given dataframe 'data' and parameter eta
#Each column represents a specialist, except for the first one that is the date
def multiplicative_weigths (data, eta):
    #gets the number of specialists and set the initial gains vector
    specialists_num=len(data.columns)-1
    gains_vec= [1] * specialists_num

    #Creates results columns
    data['Chosen Specialist'] = ['None'] * len(data)
    data['Result'] = [0.0] * len(data)

    for index, row in data.iterrows():
        chosen_specialist = make_distributed_decision(gains_vec)+1
        chosen_specialist = data.columns[chosen_specialist]

        data.set_value(index, 'Chosen Specialist', chosen_specialist)
        data.set_value(index, 'Result', data.get_value(index,chosen_specialist))

        for specialist in range(1,specialists_num+1):
            gains_vec[specialist-1]= gains_vec[specialist-1]*(1+data.get_value(index,data.columns[specialist]))

        #print("This is the row: %s") % row
        #print("This is the date: %s") % row[[0]]
        #for specialist in range(1,specialists_num+1):
        #    print ("This is specialist number %d value: %f") % (specialist, row[[specialist]])
    return data
