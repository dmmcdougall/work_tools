
import pandas as pd
import db_functions as dbfnc
import config as cfg

def main():
    # grab a list of tables form the db
    query = ("SELECT * FROM INFORMATION_SCHEMA.TABLES\
        WHERE TABLE_TYPE = 'BASE TABLE'")

    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        df = pd.read_sql(query, conn)

    list_of_tbl = df.TABLE_NAME.to_list()

    # some of the tables have restricted characters, make all table names readable
    new_list = []
    for tbl in list_of_tbl:
        new_str = '['+tbl+']'
        new_list.append(new_str)

    # save each table as a .csv
    for i in new_list:
        query = (f'SELECT * FROM {i}')
        with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
            df = pd.read_sql(query, conn)
        
        print(i)
        print(df.head(5))
        print()
        
        df.to_csv(f'{cfg.desktop_dir}/{i}.csv', index=False)

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                      file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
