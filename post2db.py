'''

'''

# standard library
import os
import pandas as pd
import pyodbc
import sqlalchemy as sa

# third party libraries

# local repo
import config as cfg
import databaseFunctions as dbfnc

# at this point, the new data has been scrapped from the timesheet and added to
# a .xls file

def main():

    # put the new data into a df
    cols_to_use = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    df_scraped = pd.read_excel(cfg.home+"\\Desktop\\scraped_by_python.xls", usecols=cols_to_use)

    # find the number we need to start the new data with
    query = "SELECT * FROM HeadShiftWorkedTable"
    df_hShift = pd.read_sql(query, cfg.conn)
    last_shift = df_hShift['HeadShiftWorkedID'].max()
    # print(last_shift) # for testing
    new_shift = last_shift +1

    # put the new shiftIDs into the df
    shift_list = []

    for i in range(len(df_scraped['HeadIDLetter'])):
        shift_list.append(new_shift+i)

    df_scraped.insert(0,'Shift', shift_list)
    df_scraped.set_index('Shift')

    # send the df to the db
    tbl = 'TMPtblWeeklyHeadsData'
    tbl_exist = dbfnc.checkTableExists(cfg.conn, tbl)

    if tbl_exist == True:
        print("let's empty the table")
        cur = cfg.conn.cursor()
        # cur.execute("TRUNCATE Table TMPtblWeeklyHeadsData")
        cur.execute("DROP Table TMPtblWeeklyHeadsData")
        cfg.conn.commit()

    else:
        print("let's build the table")
        # with engine.connect() as con:
        #     con.execute('ALTER TABLE TMPtblWeeklyHeadsData ADD PRIMARY KEY (Shift);')
        print("OOPS! IF YOU ARE READING THIS WE HAVE A PROBLEM!")
        print("NEXT COMES THE ERROR MESSAGE!")

    print("Table path cleared, let's write to the db")
    engine = sa.create_engine(cfg.alc_str)
    df_scraped.to_sql(tbl,
                      con=engine,
                      if_exists = 'append',
                      index = False,
                      dtype={'Shift':sa.types.INT,
                             'HeadIDLetter':sa.types.NVARCHAR(length=255),
                             'HeadIDNumber':sa.types.INT,
                             'Date': sa.dialects.mssql.DATETIME2(0),
                             'InTime': sa.dialects.mssql.DATETIME2(0),
                             'OutTime': sa.dialects.mssql.DATETIME2(0),
                             'EventYrID':sa.types.NVARCHAR(length=255),
                             'EventID': sa.types.NVARCHAR(length=255),
                             'Reg': sa.types.FLOAT,
                             'OT': sa.types.FLOAT,
                             'Double': sa.types.FLOAT,
                             'Acct':sa.types.NVARCHAR(length=255),
                             'Blackscall': sa.dialects.mssql.BIT,
                             'MP': sa.dialects.mssql.BIT}
                      )

    cfg.conn.close()

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                 post_2db.py file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()