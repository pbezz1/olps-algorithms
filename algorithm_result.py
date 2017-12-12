'''
Created on Dec 4, 2017

@author: ckubudi
'''
import pandas as pd
import numpy as np
import os


class AlgorithmResult():
    
    def calculate(self):
        pass
    
    def __init__(self, data, name):
        self.data=data
        temp=data['result']+1
        self.r_log=np.log(temp)
        self.r_cum = temp.cumprod()
        self.r_cum_log=np.log(self.r_cum)
        self.name=name
        self.benchmarks=[]
        self.calculate()
    
    def add_benchmark(self,file_path):
        """Adds benchmarks to algo result
        :file_path path to csv with results from algorithm
        """
        benchmark_name=os.path.basename(file_path)
        benchmark_name=os.path.splitext(benchmark_name)[0]
        if(benchmark_name in self.data.columns):
            return benchmark_name
        benchmark_data=pd.DataFrame.from_csv(file_path)
        if(len(benchmark_data.columns) != 1):
            raise Exception('something is wrong with benchmark file')
            return
        benchmark_data.columns=[benchmark_name]
        self.data = self.data.join(benchmark_data, how='left')
        self.benchmarks.append(benchmark_name)
        return benchmark_name
        
    @property
    def yrly_roa(self):
        roa = self.r_cum_log[len(self.r_cum_log)-1] / self.max_drawdown
        return roa/(len(self.data)/252.)
    
    @property
    def total_equity(self):
        return self.equity[len(self.data)-1]-1
    
    @property
    def equity(self):
        return self.r_cum
    
    @property
    def drawdown_period(self):
        ''' Returns longest drawdown perid. Stagnation is a drawdown too. '''
        x = self.equity
        period = [0.] * len(x)
        peak = 0
        for i in range(len(x)):
            # new peak
            if x[i] > peak:
                peak = x[i]
                period[i] = 0
            else:
                period[i] = period[i-1] + 1
        return max(period) * 252. / 252

    @property
    def max_drawdown(self):
        ''' Returns highest drawdown'''
        x = self.r_cum_log
        return max(x.cummax()-x)
    
    @property
    def winning_pct(self):
        x = self.data['result']
        win = (x > 0).sum()
        all_trades = (x != 0).sum()
        return float(win) / all_trades
    
    @property
    def annualized_return(self):
        return np.exp(self.r_log.mean() * 252.) - 1

    @property
    def annualized_volatility(self):
        return np.exp(self.r_log).std() * np.sqrt(252.)
    
    
    @property
    def sharpe(self):
        """ Compute annualized sharpe ratio from log returns. 
        """
        freq = 252.
        mu, sd = self.r_log.mean(), self.r_log.std()
        mu = mu * freq
        sd = sd * np.sqrt(freq)
        
        return mu/sd
    
    
    def summary(self):
        return """Summary:
        Yrly ROA: {:.2f}
        Yrly Sharpe Ratio: {:.2f}
        Annualized return: {:.2f}%
        Annualized volatility: {:.2f}%
        Longest drawdown: {:.0f} days
        Net Return: {:.2f}%
        Winning days: {:.1f}%
        Start Date: {:%m/%Y}
        End Date: {:%m/%Y}
        """.format(self.yrly_roa,self.sharpe,
                   100*self.annualized_return,
                   100*self.annualized_volatility,
                   self.drawdown_period,
                   100*self.total_equity,
                   100*self.winning_pct, 
                   self.data.index[0],
                   self.data.index[len(self.data)-1])
        
    def get_hedged_result(self, file_path, proportion = 1.0):
        """Returns the algorithm result for the hedged curve against the benchmark
        :file_path path to benchmark file
        """
        b_name=self.add_benchmark(file_path)
        new_data=self.data.copy(deep=True)
        new_data['result']=new_data['result']-(new_data[b_name]*proportion)
        return AlgorithmResult(new_data[['result']],self.name+" hedged")
        
        
    def plot(self, **kwargs):
        columns=self.benchmarks[:]
        df = self.data[columns]
        for column in self.benchmarks:
            df[column]=df[column]+1
            df[column]= np.log(df[column].cumprod())
        df[self.name]=self.r_cum_log
        df.plot(legend=True,linewidth=0.5, **kwargs)
        
    def plot_yrly_result(self, **kwargs):
        df = self.data[['result']+self.benchmarks]
        df=df+1
        df = pd.groupby(df,by=[df.index.year]).prod()
        df=df-1
        df=df*100
        df.rename(columns={'result':self.name},inplace=True)
        df.plot.bar(legend=True, **kwargs)
        
class AlgorithmResultsList():

    def __init__(self, results = []):
        self.data=None
        for result in results:
            self.update_data(result)

    def update_data(self, result):
        if(self.data is None):
            self.data=pd.DataFrame(result.r_cum_log)
        else:
            self.data=self.data.join(pd.DataFrame(result.r_cum_log), how='outer')
        self.data.rename(columns={'result':result.name}, inplace=True)
    
    def add_benchmark(self,file_path):
        """Adds benchmarks to algo result
        :file_path path to csv with results from algorithm
        """
        benchmark_name=os.path.basename(file_path)
        benchmark_name=os.path.splitext(benchmark_name)[0]
        if(benchmark_name in self.data.columns):
            return
        benchmark_data=pd.DataFrame.from_csv(file_path)
        if(len(benchmark_data.columns) != 1):
            raise Exception('something is wrong with benchmark file')
            return
        benchmark_data.columns=[benchmark_name]
        self.data = self.data.join(benchmark_data, how='left')
        self.data[benchmark_name]=self.data[benchmark_name]+1
        self.data[benchmark_name]=np.log(self.data[benchmark_name].cumprod())
        
    def append(self, item):
        if not isinstance(item, AlgorithmResult):
            raise TypeError('item is not an algorithm result')
        self.update_data(item)
        
    def plot(self, **kwargs):
        self.data.plot(legend=True,linewidth=0.5, **kwargs)
    
        
    
    
    
    
    
    
    
    
    
