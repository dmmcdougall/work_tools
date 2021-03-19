import pandas as pd
import db_functions as dbfnc
import config as cfg
from datetime import date

# grab data from the db
sql_file=open(f'{cfg.sql_dir}\head_toil_days.sql')
query = sql_file.read()

with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
    df = pd.read_sql(query, conn)

# filter for last 24 months
value_to_check = pd.Timestamp((date.today().year-2), date.today().month, date.today().day)
filter_mask = df['ShiftDate'] > value_to_check
df = df[filter_mask]

# turn the datetime64 object into a string object for manipultaion
df['Date_String'] = df['ShiftDate'].dt.strftime('%Y-%m-%d')

# create the fiscal info from teh new string object
df['Fiscal Year'] = df.Date_String.apply(dbfnc.fiscal_yr)
df['Fiscal Quarter'] = df.Date_String.apply(dbfnc.fiscal_q)

# sort for presentation
df.sort_values(by='FirstName', inplace=True)
sort_list = ['Fiscal Year', 'Fiscal Quarter']
df.sort_values(by=sort_list, ascending=False, inplace=True)

print(df.head(75))
# print(df.info())