'''
Created on Dec 4, 2017

@author: ckubudi
'''
import pandas as pd
import os


class AlgorithmResult():
    
    def calculate(self):
        pass
    
    def __init__(self, data, name):
        self.data=data
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
            return
        benchmark_data=pd.DataFrame.from_csv(file_path)
        if(len(benchmark_data.columns) != 1):
            raise Exception('something is wrong with benchmark file')
            return
        benchmark_data.columns=[benchmark_name]
        self.data = self.data.join(benchmark_data, how='left')
    
    @property
    def yrly_roa(self):
        roa = self.data['result'].sum() / self.max_drawdown
        return roa/(len(self.data)/252.)
    
    @property
    def equity(self):
        return self.data['result'].cumsum()
    
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
        ''' Returns highest drawdown in percentage. '''
        x = self.equity
        return max(1. - x / x.cummax())
    
    @property
    def winning_pct(self):
        x = self.data['result']
        win = (x > 0).sum()
        all_trades = (x != 0).sum()
        return float(win) / all_trades
    
    
    def summary(self):
        return """Summary:
        Yrly ROA: {:.2f}
        Longest drawdown: {:.0f} days
        Max drawdown: {:.2f}%
        Winning days: {:.1f}%""".format(self.yrly_roa,self.drawdown_period,100 * self.max_drawdown,100 * self.winning_pct)
        
    def plot(self, **kwargs):
        columns=self.data.columns[1:len(self.data.columns)]
        df = self.data[columns]
        for column in df.columns:
            df[column]= df[column].cumsum()
        df=df.rename(columns={'result' : self.name})
        df.plot(legend=True, **kwargs)
