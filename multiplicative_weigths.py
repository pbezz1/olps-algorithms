from __future__ import division
import numpy as np
from algorithm import Algorithm


class Multiplicative_Weights(Algorithm):
    
    def __init__(self, eta, period, beta=None):
        """Runs the multiplicative weigths algorithm
        :eta: learning rate parameter
        :period: business days between each rebalance
        :beta: fixed share parameter. if none is given, the original version of the algorithm is used
        """
        super(Multiplicative_Weights, self).__init__()
        self.eta=eta
        self.period=period
        self.beta=beta
        self.periodOffset=period
        self.update_returns=[]
        
    @staticmethod
    def normalize(vec):
        """returns normalized version of vec
        :vec: vector of numbers
        """
        #calculate vec sum
        vec_sum=0
        for elem in vec:
            vec_sum+=elem
    
        #calculate probabilities
        probabilities_list = []
        for elem in vec:
            probabilities_list.append(elem/vec_sum)
    
        return probabilities_list
    
    def multiplicative_weigths_linear_update(self, update_returns, gains_vec, specialists_num):     
        """Linear update rule for multiplicative weigths method
        not in use"""
        for specialist in range(specialists_num):
            gains_vec[specialist] = gains_vec[specialist] * ((1 + self.eta) * update_returns[specialist]-1)
        
        gains_vec = self.normalize(gains_vec)
        
        return gains_vec
    
    
    def multiplicative_weigths_exp_update(self, update_returns, gains_vec, specialists_num):
        """Exponential update rule for multiplicative weigths method
        """
        for specialist in range(specialists_num):
            gains_vec[specialist] = gains_vec[specialist] * np.exp(self.eta * (update_returns[specialist]-1))
        
        gains_vec = self.normalize(gains_vec)
    
        return gains_vec
    
    def adaptive_regret_update(self, update_returns, gains_vec, specialists_num):
        """Implements the adaptive regret rule for both static and dynamic beta values
        """
        gains_vec = self.multiplicative_weigths_exp_update(update_returns, gains_vec, specialists_num)
    
        myBeta=self.beta
        #if(isinstance(beta, (list, np.ndarray))):
        #    myBeta=beta[index]
        
        for specialist in range(specialists_num):
            gains_vec[specialist] =(myBeta/specialists_num)+((1-myBeta)*gains_vec[specialist])
        
        gains_vec = self.normalize(gains_vec)
    
        return gains_vec
    
    def before_backtest(self, data):
        specialists_num=len(data.columns)-1
        self.update_returns=[1] * specialists_num 
        self.update_data=data
        return data
    
    def update_weights(self,current_index, current_weights, data):        #assertive: if the mode is adaptive regret and there is no beta defined, then a warning is raised
        specialists_num=len(data.columns)-1
        
        for specialist in range(specialists_num):
            self.update_returns[specialist] = self.update_returns[specialist] * (1+self.update_data.get_value(current_index, self.update_data.columns[specialist+1]))
     
        #if period has passed, update gains vector
        if(self.periodOffset>=self.period):
            if(self.beta is None):
                weights_vec = self.multiplicative_weigths_exp_update(self.update_returns, current_weights , specialists_num)
            else:
                weights_vec = self.adaptive_regret_update(self.update_returns, current_weights, specialists_num)
            #reset returns for the next period
            self.update_returns= [1] * specialists_num
            self.periodOffset=0
        else:
            weights_vec=current_weights
            
        self.periodOffset=self.periodOffset+1     
          
        return weights_vec
