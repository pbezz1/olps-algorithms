from enum import Enum
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
#'data' must have the first column representing the periods (dates) and all of the others are each a specialist
def multiplicative_weigths (data, eta):
    #gets the number of specialists and set the initial gains vector
    specialists_num=len(data.columns)-1
    gains_vec= [1] * specialists_num

    #Creates results columns
    data['Result'] = [0] * len(data)
    data['Chosen Specialist'] = ['None'] * len(data)

    for index, row in data.iterrows():
        chosen_specialist = make_distributed_decision(gains_vec)
        print("This is the row: %s") % row
        print("This is the date: %s") % row[[0]]
        for specialist in range(1,specialists_num+1):
            print ("This is specialist number %d value: %f") % (specialist, row[[specialist]])
    return
