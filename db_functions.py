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

@contextmanager
def connection(my_driver, my_server, my_db):
    """This context manager takes care of the connection, commits, and closes associated with database servers.

    :param my_driver: Your installed ODBC driver.
    :type my_driver: string
    :param my_server: Your server name.
    :type my_server: string
    :param my_db: Your database name.
    :type my_db: string
    :return: a server connection
    :rtype: string
    """
    connection = pyodbc.connect(
        f"Driver={my_driver};"
        f"Server={my_server};"
        f"Database={my_db};"
        "Trusted_Connection=yes;"
    )
    # make the connection
    try:
        logger.info('Connecting to database')
        yield connection
    # if connection fails, rollback and raise an error
    except Exception:
        logger.info('***Connection to database FAILED***')
        connection.rollback()
        raise
    # commit the transaction
    else:
        connection.commit()
    # always close try to close the connection
    finally:
        connection.close()
        logger.info('Closing connection to database')

def find_crew_Alpha_number(crew_name):
    """This query takes a "FirstName LastName" string of a
    casual crew member and returns the alphabetic portion
    of an employee number from the database. This can take
    a legal first name or a preferred name.

    :param crew_name: This is a proper name such as "Willy Wonka".  Legal first names or preferred names accepted.
    :type crew_name: string
    :return: Employee alpha number for casual crew member as string
    :rtype: string
    """
    logger.info(f'the function find_crew_alpha_number2 recieved this argument: {crew_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        # the full name is likely pulled from an excel form with full name field.
        # let's split the full name into a first name and a last name.
        mylist = (str.split(crew_name))

        # First, assume this is a legal first name.
        try:
            first_name_query = conn.execute("""
                  SELECT CrewIDAlpha FROM CrewNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (first_name_query.fetchone())
            return my_record[0]
        # If that fails, infor the user and check the preferred name field
        except TypeError:
            print("The find_crew_Alpha_number2 method found no matching name, checking preferred names...")
            print()
            try:
                prefer_name_query = conn.execute("""
                    SELECT CrewIDAlpha FROM CrewNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (prefer_name_query.fetchone())
                return my_record[0]
            # And if that fails as well, forward the issue to the user.
            except:
                print('The name on this timesheet is not in the CrewNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

def find_crew_number(crew_name):
    """This query takes a "FirstName LastName" string of a
    casual crew member and returns the numeric portion of
    an employee number from the production database.
    This can take a legal first name or a preferred name.

    :param crew_name: This is proper a name such as "Willy Wonka".  Legal first names or preferred names accepted.
    :type crew_name: string
    :return: Employee number for casual crew member as string
    :rtype: string
    """
    logger.info(f'the function find_crew_number2 recieved this argument: {crew_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        # the full name is likely pulled from an excel form with full name field.
        # let's split the full name into a first name and a last name.
        mylist = (str.split(crew_name))

        # First, assume this is a legal first name.
        try:
            first_name_query = conn.execute("""
                  SELECT CrewID FROM CrewNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (first_name_query.fetchone())
            return my_record[0]
        # If that fails, infor the user and check the preferred name field
        except TypeError:
            print("The find_crew_number2 method found no matching name, checking preferred names...")
            print()
            try:
                prefer_name_query = conn.execute("""
                    SELECT CrewID FROM CrewNamesTable
                    WHERE preferred_name = ?
                    AND LastName = ?
                """, (mylist[0], mylist[1]))
                my_record = (prefer_name_query.fetchone())
                return my_record[0]
            # And if that fails as well, forward the issue to the user.
            except:
                print('The name on this timesheet is not in the CrewNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

def find_head_alpha_number(head_name):
    """This query takes a "FirstName LastName" string of a
    salaried head staff member and returns the alphabetic portion
    of an employee number from the database. This can take a legal
    first name or a preferred name.

    :param head_name: This is a proper name such as "Willy Wonka".  Legal first names or preferred names accepted.
    :type head_name: string
    :return: Employee alpha number for a salaried head staff member as string
    :rtype: string
    """
    logger.info(f'the function find_head_alpha_number2 recieved this argument: {head_name}')
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        # the full name is likely pulled from an excel form with full name field.
        # let's split the full name into a first name and a last name.
        mylist = (str.split(head_name))

        # First, assume this is a legal first name.
        try:
            fname_query = conn.execute("""
                  SELECT HeadIDAlpha FROM HeadNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        # If that fails, infor the user and check the preferred name field
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
            # And if that fails as well, forward the issue to the user.
            except:
                print('The name on this timesheet is not in the HeadNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

def find_head_number(head_name):
    """This query takes a "FirstName LastName" string of a
    salaried head staff member and returns the numeric portion of
    an employee number from the production database.
    This can take a legal first name or a preferred name.

    :param head_name: This is a proper name such as "Willy Wonka".  Legal first names or preferred names accepted.
    :type head_name: string
    :return: Employee alpha number for a salaried head staff member as string
    :rtype: string
    """
    logger.info(f'the function find_head_number2 recieved this argument: {head_name}')
    # the full name is likely pulled from an excel form with full name field.
    # let's split the full name into a first name and a last name.
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        mylist = (str.split(head_name))

        # First, assume this is a legal first name.
        try:
            fname_query = conn.execute("""
                  SELECT HeadID FROM HeadNamesTable
                  WHERE FirstName = ?
                  AND LastName = ?
              """, (mylist[0], mylist[1]))
            my_record = (fname_query.fetchone())
            return my_record[0]
        # If that fails, infor the user and check the preferred name field
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
            # And if that fails as well, forward the issue to the user.
            except:
                print('The name on this timesheet is not in the HeadNamesTable of the database.')
                print("Please check the name on this timesheet against current records.")

def find_next_row_from_db(my_table, my_column):
    """This function returns the next available identity value for a database table

    :param my_table: The table to be examined.
    :type my_table: string
    :param my_column: The column to be examined.
    :type my_column: string
    :return: The next available row index as an integer
    :rtype: string
    """
    with connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        query = ("SELECT * FROM ?", my_table)
        table_df = pd.read_sql(query, conn)
        last_id_num = table_df[my_column].max()
        new_id_num = last_id_num + 1
        return new_id_num

def grabeventYR2(datestr):
    """Using a date string, create an eventID year value.

    :param datestr: a date string in the required format of yyyy/mm/dd
    :type datestr: string
    :return: A date code in the form of a single letter as a string
    :rtype: string
    """
    # split the string into [year, month, date]
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

    # build some useful variables
    yr_strt = 2011 # the first year, year 'A'
    mos_strt = 9 # fiscal years are sept-aug so calendar month 9==1, and cal mos 8==12
    yr_diff = yr_int - yr_strt
    mos_diff = mos_int - mos_strt

    # In 2019, the letter 'I' was skipped.  the years went ...'F', 'G', 'H', 'J', 'K'...
    # This is for 2019
    if yr_int == 2019:
        # This is the fiscal year adjustments
        if mos_int < mos_strt:
            # The first half of 2019
            # This is the fiscal year adjustments
            if mos_diff < 0:
                alphayr = ord('A') + yr_diff - 1
            else:
                alphayr = ord('A') + yr_diff
        else:
            # The second half of 2019
            # This is the fiscal year adjustments
            if mos_diff < 0:
                alphayr = ord('A') + yr_diff
            else:
                alphayr = ord('A') + yr_diff +1
    # This is for 2019 or later
    elif yr_int > 2019:
        # This is the fiscal year adjustments
        if mos_diff < 0:
            alphayr = ord('A') + yr_diff
        else:
            alphayr = ord('A') + yr_diff + 1
    # This is for 2019 or earlier
    else:
        # This is the fiscal year adjustments
        if mos_diff < 0:
            alphayr = ord('A')+yr_diff-1
        else:
            alphayr = ord('A')+yr_diff

    return chr(alphayr)

def fiscal_q(my_date):
    date_tup = str.split(my_date, '-')

    cal_mos = int(date_tup[1])

    if cal_mos >= 1 and cal_mos <=2:
        fis_q = 2
    elif cal_mos >= 3 and cal_mos <=5:
        fis_q = 3
    elif cal_mos >= 6 and cal_mos <=8:
        fis_q = 4
    elif cal_mos >= 9 and cal_mos <=11:
        fis_q = 1
    else:
        fis_q = 2

    return fis_q

def fiscal_yr(my_date):
    date_tup = str.split(my_date, '-')

    cal_yr = date_tup[0]
    cal_mos = date_tup[1]

    if int(cal_mos) < 9:
        fis_yr = str(int(cal_yr)-1) + "-" + str(cal_yr)
    else:
        fis_yr = str(int(cal_yr)) + "-" + str(int(cal_yr)+1)

    return fis_yr    

######## SIMPLE SQL QUERIES THAT WORK BUT ARE UNUSED FOR NOW #######

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


