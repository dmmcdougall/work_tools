import pandas as pd
import db_functions as dbfnc
import config as cfg
from datetime import date

# grab data from the db and input it to a df
# the query is HeadworkedTable joined with ShowTable joined with HeadNamesTable filtered on ShowName 'FLEX DAY'
sql_file=open(f'{cfg.sql_dir}\TOIL_payouts.sql')
query = sql_file.read()

with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
    df = pd.read_sql(query, conn)



df['Date_String'] = df['PayoutDate'].dt.strftime('%Y-%m-%d')
filter_mask = df.Date_String.apply(dbfnc.current_fiscal) 
df = df[filter_mask]

print(df.head(10))