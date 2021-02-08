"""
The dbfnc sheet is for queries to the SQL server.
"""

# standard library
import logging
import pyodbc
import pandas as pd
from contextlib import contextmanager

# third part libraries
import config as cfg

# local repo

# logging info
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # change to DEBUG when required

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(cfg.log_files + '\\' + 'databaseFunctions.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# this context manager takes care of the conn commits and closes.
@contextmanager
def connection(my_driver, my_server, my_db):
    connection = pyodbc.connect(
        f"Driver={my_driver};"
        f"Server={my_server};"
        f"Database={my_db};"
        "Trusted_Connection=yes;"
    )
    try:
        logger.info('Connecting to database')
        yield connection
    except Exception:
        logger.info('***Connection to database FAILED***')
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()
        logger.info('Closing connection to database')

# this query takes a "FirstName lastName" of a Casual Crew member and returns
#  the numeric portion of an employee number
def find_crew_number2(crew_name):
    logger.info(f'the function find_crew_number2 recieved this argument: {crew_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        mylist = (str.split(crew_name))

        try:
            fname_query = conn.execute("""
                  SELECT CrewID FROM CrewNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        except TypeError:
            print("The find_crew_number2 method found no matching name, checking preferred names...")
            print()
            try:
                pname_query = conn.execute("""
                    SELECT CrewID FROM CrewNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (pname_query.fetchone())
                return my_record[0]
            except:
                print('The name on this timesheet is not in the CrewNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

# this query takes a "FirstName lastName" of a Casual Crew member and returns
# the Alhabetical portion of an employee number
def find_crew_Alpha_number2(crew_name):
    logger.info(f'the function find_crew_alpha_number2 recieved this argument: {crew_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        mylist = (str.split(crew_name))

        try:
            fname_query = conn.execute("""
                  SELECT CrewIDAlpha FROM CrewNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        except TypeError:
            print("The find_crew_Alpha_number2 method found no matching name, checking preferred names...")
            print()
            try:
                pname_query = conn.execute("""
                    SELECT CrewIDAlpha FROM CrewNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (pname_query.fetchone())
                return my_record[0]
            except:
                print('The name on this timesheet is not in the CrewNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

# this query takes a "FirstName lastName" of a Salaried Head staff member and returns
# the Alhabetical portion of an employee number
def find_head_alpha_number2(head_name):
    logger.info(f'the function find_head_alpha_number2 recieved this argument: {head_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        mylist = (str.split(head_name))

        try:
            fname_query = conn.execute("""
                  SELECT HeadIDAlpha FROM HeadNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        except TypeError:
            print("The find_head_alpha_number2 method found no matching name, checking preferred names...")
            print()
            try:
                pname_query = conn.execute("""
                    SELECT HeadIDAlpha FROM HeadNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (pname_query.fetchone())
                return my_record[0]
            except:
                print('The name on this timesheet is not in the HeadNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

# this query takes a "FirstName lastName" of a Salaried Head Staff member and returns
#  the numeric portion of an employee number
def find_head_number2(head_name):
    logger.info(f'the function find_head_number2 recieved this argument: {head_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        mylist = (str.split(head_name))

        try:
            fname_query = conn.execute("""
                  SELECT HeadID FROM HeadNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        except TypeError:
            print("The find_head_number2 method found no matching name, checking preferred names...")
            print()
            try:
                pname_query = conn.execute("""
                    SELECT HeadID FROM HeadNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (pname_query.fetchone())
                return my_record[0]
            except:
                print('The name on this timesheet is not in the HeadNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

# find the number we need to start the new data with by checking where
# the ShiftID numbering ended
def find_next_row_from_db(my_table, my_column):
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        query = ("SELECT * FROM ?", my_table)
        df_hShift = pd.read_sql(query, conn)
        last_shift = df_hShift[my_column].max()
        new_shift = last_shift + 1
        return new_shift

# Using the Date string, create an event ID
def grabeventYR2(datestr):
    if datestr[4] == '/':
        newdate = str.split(datestr, '/')
    elif datestr[4] == '-':
        newdate = str.split(datestr, '-')
    else:
        print("****************ERROR******************")
        print("Your 'Grab Event Year' method is broken")
        print("****************ERROR******************")
    yr_int = int(newdate[0])
    mos_int = int(newdate[1])
    yr_strt = 2011
    mos_strt = 9
    yr_diff = yr_int - yr_strt
    mos_diff = mos_int - mos_strt

    if yr_int == 2019:
        if mos_int < mos_strt:
            if mos_diff < 0:
                alphayr = ord('A') + yr_diff - 1
            else:
                alphayr = ord('A') + yr_diff
        else:
            if mos_diff < 0:
                alphayr = ord('A') + yr_diff
            else:
                alphayr = ord('A') + yr_diff +1
    elif yr_int > 2019:
        if mos_diff < 0:
            alphayr = ord('A') + yr_diff
        else:
            alphayr = ord('A') + yr_diff + 1
    else:
        if mos_diff < 0:
            alphayr = ord('A')+yr_diff-1
        else:
            alphayr = ord('A')+yr_diff

    return chr(alphayr)

# GENERIC SQL QUERIES THAT WORK

# read from SQL and print to screen
def read2screen(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row)

# read from SQL without printing
def read2(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)

# general method
def general(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

# does your table exist?
def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def drop_table(self, table):
    pass
    #self._exec(schema.DropTable(table))


if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')


