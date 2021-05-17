
import pandas as pd
import db_functions as dbfnc
import config as cfg

query = ("SELECT * FROM INFORMATION_SCHEMA.TABLES\
     WHERE TABLE_TYPE = 'BASE TABLE'")

with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
    df = pd.read_sql(query, conn)

list_of_tbl = df.TABLE_NAME.to_list()

new_list = []
for tbl in list_of_tbl:
    new_str = '['+tbl+']'
    new_list.append(new_str)

for i in new_list:
    query = (f'SELECT * FROM {i}')
    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        df = pd.read_sql(query, conn)
    
    print(i)
    print(df.head(5))
    print()
    
    df.to_csv(f'{cfg.desktop_dir}/{i}.csv')

