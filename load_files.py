import numpy as np
import pandas as pd
import os
from datetime import datetime

#loads the specified csv to an array
def load_file(path):
    data = np.loadtxt(path, delimiter=',', dtype=object,converters={0: lambda x: datetime.strptime(x, "%m/%d/%Y")})
    return data

#builds data dictionary with all files in a path synchronized
def build_data(directory):
    dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            data = load_file(os.path.join(directory,filename))
            dict[os.path.splitext(filename)[0]] = data

    return dict

def build_data_2(directory):
    dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            data = load_file(os.path.join(directory,filename))
            dict[os.path.splitext(filename)[0]] = data

    d1 = pd.DataFrame(dict('PETR3'))
    d2 = pd.DataFrame(dict('BOVA11'))
    d1.columns = d2.columns = ['date','return']

    result = pd.DataFrame(np.array(d1.merge(d2, on='date', how='outer').sort('date')), columns= ['date','petr3','bova11'])

    return result




#dict = build_data('data/')

result = build_data_2('data/')

print("finished")

