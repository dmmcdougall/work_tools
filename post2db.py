# standard library
import os
import pandas as pd
import pyodbc

# third party libraries

# local repo
import config as cfg
import databaseFunctions as dbfnc

# at this point, the new data has been scrapped from the timesheet and added

def main():

    # put the new data into a df
    cols_to_use = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    df_scraped = pd.read_excel(cfg.home+"\\Desktop\\scraped_by_python.xls", index='Shift', usecols=cols_to_use)

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
    
    df_scraped.to_excel(cfg.home+"\\Desktop\\scraped_with_shiftNum.xls")

    os.system(f"start EXCEL.EXE {cfg.home}\Desktop\scraped_with_shiftNum.xls")

    # !!!!! IS IT POSSIBLE ONE CANNOT CONNECT TO ACCESS WITH 64-BIT PYTHON!!!!
    # connect to MS Access
    # conn2 = pyodbc.connect(
    #     "Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    #     "DBQ=C:\\Users\\dmcdougall\\Desktop\\test.accdb;"
    # )
    #
    # cursor = conn2.cursor()
    # cursor.execute('select * from TMP-HeadsImport')
    #
    # for row in cursor.fetchall():
    #     print(row)

    # clear the tmp table
    # query = 'TRUNCATE TABLE  TMP-HeadsImport;'
    # fnc.delete(conn, query)

    # to read into df
    #views = pd.read_sql(query, conn)

    cfg.conn.close()

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("              post_2db.py file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()