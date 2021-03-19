import pandas as pd
import db_functions as dbfnc
import config as cfg

dates = pd.to_datetime(pd.Series(['20010101', '20010331']), format = '%Y%m%d')
dates.dt.strftime('%Y-%m-%d')

print(dates)
