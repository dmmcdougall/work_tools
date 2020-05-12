# standard library
import pandas as pd
import pyodbc

# third party libraries

# local repo
import config as cfg
import myFunctions as db

conn = pyodbc.connect(
    "Driver={ODBC Driver 13 for SQL Server};"
    "Server=CGYSQL01\MISC;"
    "Database=production;"
    "Trusted_Connection=yes;"
)

def main():

    # to print to screen
    #db.read(conn, query)
    # to read into df
    #views = pd.read_sql(query, conn)

    cols_to_use = [1,2,3,4,5,6,7,8,9,10,11,12,13]

        #put the new data into a df
    df_scraped = pd.read_excel(cfg.home+"\\Desktop\\scraped_by_python.xls", index='Shift', usecols=cols_to_use)

    # find the number we need to start the new data with

    query = "SELECT * FROM HeadShiftWorkedTable"
    df_hShift = pd.read_sql(query, conn)
    last_shift = df_hShift['HeadShiftWorkedID'].max()
    print(last_shift)
    new_shift = last_shift +1

    # put the new shiftIDs into the df

    shift_dict = {}
    shift_list = []

    for i in range(len(df_scraped['HeadIDLetter'])):
        shift_list.append(new_shift+i)

    df_scraped.insert(0,'Shift', shift_list)

    #df_scraped['Shift'].replace(,[shift_list])

    #df_scraped = df_scraped.append(pd.DataFrame(shift_dict), inplace=True)




    df_hShift.loc['ShiftID', shift_list]


    # clear the tmp table
    query = 'DELETE FROM  TMP-HeadsImport;'
    db.delete(conn, query)




    # to print to screen
    #db.read(conn, query)

    # to read into df
    #views = pd.read_sql(query, conn)

    conn.close()



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