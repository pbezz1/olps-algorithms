from __future__ import division
from enum import Enum
import numpy as np

def calc_probabilities(vec):
    #calculate vec sum
    vec_sum=0
    for elem in vec:
        vec_sum+=elem

    #calculate probabilities
    probabilities_list = []
    for elem in vec:
        probabilities_list.append(elem/vec_sum)

    return probabilities_list

#Makes decision based on distribution criteria given by weigths_list
def make_distributed_decision (weigths_list):
    #calculate probabilities
    probabilities_list = calc_probabilities(weigths_list)

    #sample and choose
    indexes = np.arange(0, len(weigths_list))
    index = np.random.choice(indexes , p=probabilities_list )
    return index

#Linear update rule for multiplicative weigths method
def multiplicative_weigths_linear_update(data, eta, gains_vec, specialists_num, index):
    for specialist in range(specialists_num):
            gains_vec[specialist] = gains_vec[specialist] * (1 + eta * data.get_value(index, data.columns[specialist+1]))

#Exponential update rule for multiplicative weigths method
def multiplicative_weigths_exp_update(data, eta, gains_vec, specialists_num, index):
    for specialist in range(specialists_num):
        gains_vec[specialist] = gains_vec[specialist] * np.exp(eta * data.get_value(index, data.columns[specialist+1]))

#Implements the adaptive regret rule
def adaptive_regret_update(data, eta, gains_vec, specialists_num, index, beta):
    multiplicative_weigths_exp_update(data, eta, gains_vec, specialists_num, index)

    gains_vec = calc_probabilities(gains_vec)

    for specialist in range(specialists_num):
        gains_vec[specialist] =beta*((1-beta)*gains_vec[specialist])

#Runs the multiplicative weigths algorithm based on given dataframe 'data' and parameter eta
# mode=1 is linear update; mode=2 is exponential update
#Each column represents a specialist, except for the first one that is the date
def multiplicative_weigths (data, eta, mode):
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

        if(mode==1):
            multiplicative_weigths_linear_update(data,eta,gains_vec,specialists_num,index)
        elif(mode==2):
            multiplicative_weigths_exp_update(data, eta, gains_vec, specialists_num, index)

        #print("This is the row: %s") % row
        #print("This is the date: %s") % row[[0]]
        #for specialist in range(1,specialists_num+1):
        #    print ("This is specialist number %d value: %f") % (specialist, row[[specialist]])
    return data

