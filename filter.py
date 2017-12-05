'''
Created on Dec 5, 2017

@author: ckubudi
'''
import pandas as pd


class Filter():
    def __init__(self, file_path):
        self.process_file(file_path)
        self.current_index=0 
        
    @property
    def data(self):
        return self._data

    def process_file(self, file_path):
        self._data = pd.DataFrame.from_csv(file_path, header=None)
        self._data['set']=None
        for index, row in self._data.iterrows():
            s = set(row.unique())
            self._data.set_value(index, 'set', s)
        self._data=self._data[['set']]
    
    def isWhiteListed(self,asset,date):
        """ check if given asset is tradable in given date
        :asset string with asset name
        :date datetime
        """
        if(date in self._data.index):
            row = self._data.loc[date]
            return (asset in row['set'])
        else:
            if(date < self._data.index[0]):
                return True
            else:
                raise KeyError("filter does not contain date:"+date.strftime('%m/%d/%Y'))
