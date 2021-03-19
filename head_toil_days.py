import pandas as pd
import db_functions as dbfnc
import config as cfg

# grab data from the db
sql_file=open(f'{cfg.sql_dir}\head_toil_days.sql')
query = sql_file.read()

with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
    df = pd.read_sql(query, conn)

# turn the datetime64 object into a string object for manipultaion
dates = pd.Series(df['ShiftDate'])
new_dates = dates.dt.strftime('%Y-%m-%d')
df['Date_String'] = new_dates

# create the fiscal info from teh new string object
df['Fiscal Year'] = df.Date_String.apply(dbfnc.fiscal_yr)
df['Fiscal Quarter'] = df.Date_String.apply(dbfnc.fiscal_q)

# sort for presentation
df.sort_values(by='FirstName', inplace=True)
sort_list = ['Fiscal Year', 'Fiscal Quarter']
df.sort_values(by=sort_list, ascending=False, inplace=True)

print(df.head(10))
print(df.info())