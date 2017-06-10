from __future__ import division
import numpy as np
import warnings

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
def multiplicative_weigths_exp_update(update_returns, eta, gains_vec, specialists_num, index):
    for specialist in range(specialists_num):
        gains_vec[specialist] = gains_vec[specialist] * np.exp(eta * (update_returns[specialist]-1))
    
    gains_vec = calc_probabilities(gains_vec)

    return gains_vec

#Implements the adaptive regret rule for both static and dynamic beta values
def adaptive_regret_update(data, eta, gains_vec, specialists_num, index, beta):
    multiplicative_weigths_exp_update(data, eta, gains_vec, specialists_num, index)

    gains_vec = calc_probabilities(gains_vec)

    myBeta=beta
    if(isinstance(beta, (list, np.ndarray))):
        myBeta=beta[index]

    for specialist in range(specialists_num):
        gains_vec[specialist] =(myBeta/specialists_num)+((1-myBeta)*gains_vec[specialist])

#makes a random prediction for index based on the gains_vector
def make_prediction(data,gains_vec,index):
    chosen_specialist = make_distributed_decision(gains_vec) + 1
    chosen_specialist = data.columns[chosen_specialist]

    data.set_value(index, 'Chosen Specialist', chosen_specialist)
    data.set_value(index, 'Result', data.get_value(index, chosen_specialist))
    

#Runs the multiplicative weigths algorithm based on given dataframe 'data' and parameter eta
# mode=1 is linear update; mode=2 is exponential update
#Each column represents a specialist, except for the first one that is the date
def multiplicative_weigths (raw_data, eta, mode, period, update_data, beta=None):
    #assertive: if the mode is adaptive regret and there is no beta defined, then a warning is raised
    if(mode==3 and beta==None):
         raise ValueError("No beta defined for adaptive regret")

    #assertive: if mode is adaptive regret and beta is an array, it must be the same size as data rows
    if(mode==3 and isinstance(beta, (list, np.ndarray)) and not beta.__len__() == raw_data.__len__()):
        raise ValueError("List of betas is not the same size as data points")

    data=raw_data.copy()

    #gets the number of specialists and set the initial gains vector
    specialists_num=len(data.columns)-1
    gains_vec= [1] * specialists_num

    #Creates results columns
    data['Chosen Specialist'] = ['None'] * len(data)
    data['Result'] = [0.0] * len(data)

    periodOffset=period
    
    update_returns= [1] * specialists_num
    
    for index, row in data.iterrows():
        #calculate the return of balanced portfolio
        balanced_return=0.0
        for specialist in range(specialists_num):
            balanced_return = balanced_return + (gains_vec[specialist]*data.get_value(index,data.columns[specialist+1]))

        data.set_value(index, 'Chosen Specialist', 'Balanced')
        data.set_value(index, 'Result', balanced_return)
        
        if(periodOffset>=period):
            gains_vec = multiplicative_weigths_exp_update(update_returns, eta, gains_vec, specialists_num, index)
            update_returns= [1] * specialists_num
            periodOffset=0
            
        periodOffset=periodOffset+1
        
        for specialist in range(specialists_num):
            update_returns[specialist] = update_returns[specialist] * (1+update_data.get_value(index, update_data.columns[specialist+1]))
        
    return data

#Function to build risk sensitive data as described on 
#Risk-Sensitive Online Learning paper by 
#Eyal Even-Dar, Michael Kearns, and Jennifer Wortman
def risk_sensivite(raw_data,window):
    risk_mod_data=raw_data.copy()
    columns = raw_data.columns
    for i in range(1,len(columns)):
        series=risk_mod_data[columns[i]]
        series_stdev=series.rolling(window=window,center=False).std()
        series_stdev=series_stdev.fillna(0)
        series_transform=series-series_stdev
        risk_mod_data[columns[i]]=series_transform
    return risk_mod_data