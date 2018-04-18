'''
Created on Nov 25, 2017

@author: ckubudi
'''
import numpy as np
import pandas as pd
import math
import datetime
import tqdm
from dateutil.relativedelta import relativedelta
from algorithm_result import AlgorithmResult
from profit_stop_matcher import Profit_Stop_Matcher

class Algorithm(object):
    
    def __init__(self, params={}):
        self.weights_vec=[]
        self.specialists_num=0
        self.params=params
        
        self._filter=None
        self.protit_stop_matcher=None
        #DEFAULT PARAMS
        self._set_default_parameter('rebalance_window', 1)
        self._set_default_parameter('normalize_window', 1)
        self._set_default_parameter('rebalance_period', 'monthly')
        self._set_default_parameter('cost', 0.0)
        
    def _set_default_parameter(self, param_name, param_value):
        """ Sets param with default value if it wasn't set on initialization of algorithm
        :param_name: string with name of parameter
        :param_value: param default value, type may vary
        """
        if(param_name not in self.params):
            self.params[param_name]=param_value
            
            
    def set_param(self, param_name, param_value):
        self.params[param_name]=param_value
        
        
    def set_params(self, param_dict):
        self.params.update(param_dict)
    
    def before_backtest(self, data):
        """to do before backtest
        :data: dataframe with returns and dates
        """
        #assert matcher
        if (self.protit_stop_matcher is not None):
            if(not isinstance(self.protit_stop_matcher, Profit_Stop_Matcher)):
                raise ValueError("Profit and stop was not correctly set")
            else:
                self.protit_stop_matcher.reset_trailing()
                
        #gets the number of specialists and set the initial gains vector
        self.specialists_num=len(data.columns)
        self.weights_vec=self.getUCRP_weights(self.specialists_num)
        self._last_weights=np.array([.0]*self.specialists_num)
        
        return data.loc[self.start_date:self.end_date,:]
    
    
    def update_weights(self, current_index, current_weights, data):
        """ Update the weights
        """
        return current_weights
    
    def after_backtest(self):
        """to do after backtest
        """
        pass
    
    
    def get_parameters_names(self):
        params=''
        sep=''
        for key, value in self.params.items():
            params+=sep
            params+=key
            sep=','
        return params
    
    def get_parameters_values(self):
        params=''
        sep=''
        for key, value in self.params.items():
            params+=sep
            if(isinstance(value, (int, float))):
                params+="{0:.2f}".format(value)
            else:
                params+=str(value)
            sep=','
        return params

    
    @property
    def name(self):
        return 'Algorithm'

    @staticmethod
    def getUCRP_weights(specialists_num):
        weights = [1.0/specialists_num] * specialists_num
        return weights
    
    @staticmethod
    def normalize(vec):
        """returns normalized version of vec
        :vec: vector of numbers
        """
        norm = [float(i)/sum(vec) for i in vec]
        return norm
    
    def custom_normalize(self, weights):
        long_side=weights[weights > 0.0]
        short_side=weights[weights < 0.0]
        long_sum=sum(long_side)
        short_sum=abs(sum(short_side))
        
        if(short_sum >= long_sum):
            return [0.0]*len(weights)
        
        norm = [float(i)/long_sum for i in weights]
        
        return norm
    
    def getNextUpdateDate(self, date, update_period, update_window):
        if(update_period == 'monthly'):
            date=date.replace(day=1)            
            return date + relativedelta(months=+update_window)
        else: #daily
            return date+datetime.timedelta(days=update_window)

    def getNextRebalanceDate(self, rebalance_date):
        return self.getNextUpdateDate(rebalance_date, self.params['rebalance_period'], self.params['rebalance_window'])
    
    def getNextNormalizeDate(self, normalize_date, nextRebalanceDate):
        date = self.getNextUpdateDate(normalize_date, self.params['rebalance_period'], self.params['normalize_window'])
        #date should be synchronized with rebalance date
        if(date > nextRebalanceDate):
            date=nextRebalanceDate
        return date
    
    def calculate_turnover(self, current_weights, last_weights, current_individual_returns,iteration):
        last_weights_individual_returns=current_individual_returns*last_weights
        target_rebalance=np.sum(last_weights_individual_returns)
        new_weights_individual_returns=target_rebalance*current_weights
        turnover=np.sum(np.abs(new_weights_individual_returns-last_weights_individual_returns))
        return turnover
    
    def calculate_turnover2(self, current_weights, last_weights, current_individual_returns,iteration):
        if(iteration>0):
            last_weights_individual_returns=current_individual_returns*last_weights
            target_rebalance=np.sum(last_weights_individual_returns[last_weights > 0.0])
            new_weights_individual_returns=target_rebalance*current_weights
            turnover=np.sum(np.abs(new_weights_individual_returns-last_weights_individual_returns))
            return turnover
        else:
            return 1.0 #iteration 0
    
    def trim_front(self, arr, trim_value):
        idx=0
        element=arr[idx]
        while((element == trim_value)):
            idx+=1
            if(idx >= len(arr)):
                return []
            element=arr[idx]
        return arr[idx:len(arr)]
    
    def trim_back(self, arr, trim_value):
        idx=len(arr)-1
        element=arr[idx]
        while((element == trim_value)):
            idx-=1
            if(idx<0):
                return []
            element=arr[idx]
        return arr[0:(idx+1)]
    
    def trim_result(self, result, weights_list, index):
        trim_result=self.trim_front(result, None)
        start_index=len(result)-len(trim_result)
        trim_result=self.trim_back(result,None)
        end_index=len(trim_result)
        
        trim_result=result[start_index:end_index]
        trim_weights_list=weights_list[start_index:end_index]
        trim_index=index[start_index:end_index]
        
        return (trim_result,trim_weights_list,trim_index)
        
    
    def run(self, data, start_date = '1990-01-01', end_date = '2030-01-01', show_progress_bar=False):
        """Runs the algorithm1
        :data: dataframe with each column representing a specialist, except for the first one that is the date        
        """
        self.start_date=start_date
        self.end_date=end_date
        #gets the number of specialists and set the initial gains vector

        data = self.before_backtest(data)
        
        #always rebalance on first date
        if(len(data)>0):
            rebalance_date = normalize_date = data.index[0]
        
        #create result_df dataframe
        columns = ['result']
        self._result = []
        weights_list=[]
        row_iterator=0
        current_individual_returns=np.repeat(1.0, self.specialists_num)
        total_turnover=0.0
        
        for index, row in tqdm.tqdm_notebook(data.iterrows(),total=len(data),disable=(not show_progress_bar)):
            if(index >= normalize_date):
                if(index >= rebalance_date):
                    #rebalance & normalize
                    self.weights_vec = np.array(self.update_weights(index,self.weights_vec, data.iloc[:row_iterator,:]))
                    rebalance_date=self.getNextRebalanceDate(rebalance_date)
                normalize_date=self.getNextNormalizeDate(normalize_date, rebalance_date) #next normalize date
                turnover=self.calculate_turnover(self.weights_vec,self._last_weights ,current_individual_returns,row_iterator)
                if(np.sum(self.weights_vec)!=0):
                    portfolio_return=np.dot(self.weights_vec,row)-(turnover*self.params['cost']/10000) #cost now set in bps
                else:
                    portfolio_return=None
                
                current_individual_returns=np.array(row+1)
                if((self.protit_stop_matcher is not None)):
                    self.protit_stop_matcher.reset_trailing()
                total_turnover+=turnover
            else:
                #non-rebalance date
                last_individual_returns=current_individual_returns
                current_individual_returns=np.multiply(current_individual_returns,row+1)
                if(np.sum(self.weights_vec)!=0):
                    temp1=np.dot(current_individual_returns-1,self.weights_vec)+1
                    temp2=np.dot(last_individual_returns-1,self.weights_vec)+1
                    portfolio_return=(temp1/temp2)-1 #added
                else:
                    portfolio_return=None
                    
            weights_list.append(self.weights_vec)
            self._result.append(portfolio_return)
            self._last_weights=self.weights_vec
            #check stop
            if((self.protit_stop_matcher is not None)):
                self.weights_vec = self.protit_stop_matcher.new_return(self.weights_vec, current_individual_returns)            
            row_iterator+=1
        
        self.after_backtest()

        (trim_result,trim_weights_list,trim_idx)=self.trim_result(self._result,weights_list,data.index)
        self._result = pd.DataFrame(trim_result, columns=['result'],index=trim_idx)
        weights_df=pd.DataFrame(trim_weights_list,columns=data.columns,index=trim_idx)
        
        return AlgorithmResult(self._result, self.name, weights_df,total_turnover)