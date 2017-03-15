import pandas as pd
import os

#builds data dictionary with all files in a path synchronized
def build_data(directory):
    dict = {}
    cols = ['date']
    result = None
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            data = pd.DataFrame.from_csv(os.path.join(directory,filename),index_col=None)
            data.columns = ['date','return']
            asset=os.path.splitext(filename)[0]
            cols.append(asset)
            if result is None:
                result = data
            else:
                result = result.merge(data, on='date', how='inner')

    result.columns = cols
    result['date'] = pd.to_datetime(result['date'])
    result.sort_values(by='date')

    return result