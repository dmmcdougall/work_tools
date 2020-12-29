"""
This file contains the main function for the timesheet scrapper.  The scrapper
is for taking collected timesheets, scrapping them, and placing that data
into the production database
"""

# imported from standard library
import os
import logging
import pandas as pd
import sqlalchemy as sa
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg
import databaseFunctions as dbfnc
from timesheet import TS2015, TS2011, TSCasual


# logging info
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # change to DEBUG when required

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(cfg.log_files + '\\' + 'scrape.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)



def fnc_spinner(sheet, row, my_cls, *args, **kwargs):
    for i in range(len(args)):
        func = args[i]
        function_name = func.__name__
        key_list = list(kwargs.keys())
        argument_list = [my_str for my_str in key_list if function_name in my_str]
        sorted_keys = sorted(argument_list)
        if not argument_list:
            logger.info(f'the function spinner is going to pass...{function_name}({sheet}, {row})')
            yield func(sheet, row, my_cls)
        else:
            my_val = [kwargs[x] for x in sorted_keys]
            logger.info(f'arguments for this function are {my_val}')
            logger.info(f'the function spinner is going to pass...{function_name}({sheet}, {row}, {my_val})')
            yield func(sheet, row, my_cls, *my_val)

def grab_01_head_alpha(sheet, dummy1, dummy2, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    logger.info(f'the head in question is named: {data}')
    head_alpha = dbfnc.find_head_alpha_number2(data)
    return head_alpha

def grab_01_crew_alpha(sheet, dummy1, dummy2, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    logger.info(f'the crew in question is named: {data}')
    crew_alpha = dbfnc.find_crew_Alpha_number2(data)
    return crew_alpha

def grab_02_head_id(sheet, dummy1, dummy2, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    head_id = dbfnc.find_head_number2(data)
    return head_id

def grab_02_crew_id(sheet, dummy1, dummy2, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    crew_id = dbfnc.find_crew_number2(data)
    return crew_id

def grab_03_date(sheet, row, my_cls, col):
    data = my_cls.ts_grab_date(sheet, row, col)
    return data

def grab_04_in_time(sheet, row, my_cls, col_modifier):
    data = my_cls.ts_write_time(sheet, row, col_modifier)
    return data

def grab_05_out_time(sheet, row, my_cls, col_modifier):
    data = my_cls.ts_write_time(sheet, row, col_modifier)
    return data

def grab_06_evnt_yr(sheet, row, my_cls, col_modifier):
    my_date = my_cls.ts_grab_date(sheet, row, col_modifier)
    evnt_yr = dbfnc.grabeventYR2(my_date)
    return evnt_yr

def grab_07_head_evnt_id(sheet, row, my_cls, accnt_col, date_col):
    head_acct = my_cls.ts_15_write_acct(sheet, row, accnt_col)
    my_date = my_cls.ts_grab_date(sheet, row, date_col)
    evnt_id = my_cls.ts_event_id(head_acct, my_date)
    return evnt_id

def grab_07_crew_evnt_id(sheet, row, my_cls, date_col):
    crew_acct = my_cls.ts_cas_write_acct()
    my_date = my_cls.ts_grab_date(sheet, row, date_col)
    evnt_id = my_cls.ts_event_id(crew_acct, my_date)
    return evnt_id

def grab_08_reg(sheet, row, my_cls, col):
    data = my_cls.ts_grab_hrs(sheet, row, col)
    return data

def grab_09_ot(sheet, row, my_cls, col):
    data = my_cls.ts_grab_hrs(sheet, row, col)
    return data

def grab_10_dt(sheet, row, my_cls, col):
    data = my_cls.ts_grab_hrs(sheet, row, col)
    return data

def grab_11_head_acct(sheet, row,my_cls, col):
    data = my_cls.ts_15_write_acct(sheet, row, col)
    return data

def grab_11_crew_acct(dummy, dummy1, dummy2):
    data = my_cls.ts_cas_write_acct()
    return data

def grab_12_blacks(sheet, row, my_cls, col):
    data = my_cls.ts_blacks_call(sheet, row, col)
    return data

def grab_13_MP(sheet, row, my_cls, col):
    data = my_cls.ts_mp(sheet, row, col)
    return data

def grab_14_crew_shifttype(dummy, dummy1, dummy2):
    data = 9
    return data

def create_null(dummy, dummy1, dummy2):
    data = ""
    return data

def create_eight(dummy, dummy1, dummy2):
    data = 8
    return data

def create_zero(dummy, dummy1, dummy2):
    data = 0
    return data

def kris_fix_in(sheet, row, my_cls, col, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    head_id = dbfnc.find_head_number2(data)
    if head_id == 3:
        data = my_cls.ts_15_kf_format(sheet, row, col)
        return data
    else:
        data = grab_04_in_time(sheet, row, my_cls, col)
        return data

def kris_fix_out(sheet, row, my_cls, col_modifier, name_row, name_col):
    data = sheet.cell_value(name_row, name_col)
    head_id = dbfnc.find_head_number2(data)
    if head_id == 3:
        data = my_cls.ts_15_kf_format(sheet, row, col_modifier)
        return data
    else:
        data = grab_04_in_time(sheet, row, my_cls, col_modifier)
        return data


# and this is the app...
def main():
    # set up the db column headers in lists to receive the scraped data
    # The order of these comes form teh db and is important, don't change it.
    crew_keys = ["Shift", "CrewIDLetter", "CrewIDNumber",
                 "Date", "InTime", "OutTime",
                 "EventYrID", "EventID", "Reg",
                 "OT", "Double", "Acct",
                 "Blackscall", "MP", "ShiftType"]
    head_keys = ["Shift", "HeadIDLetter", "HeadIDNumber",
                 "Date", "InTime", "OutTime",
                 "EventYrID", "EventID", "Reg",
                 "OT", "Double", "Acct",
                 "Blackscall", "MP"]

    # # Creating empty dataframes with column names only
    df_head = pd.DataFrame(columns=head_keys)
    df_crew = pd.DataFrame(columns=crew_keys)

    # find the max number in the Shift number lists so as to correctly
    # number your ShiftIDs
    # this info is pulled directly from the db
    query = "SELECT * FROM HeadShiftWorkedTable"
    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        df_h_shift = pd.read_sql(query, conn)
    head_record = df_h_shift['HeadShiftWorkedID'].max()
    next_head_num = head_record + 1

    query = "SELECT * FROM CrewShiftWorkedTable"
    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        df_c_shift = pd.read_sql(query, conn)
    crew_record = df_c_shift['ShiftWorkedID'].max()
    next_crew_num = crew_record + 1

    # create a list of the read_books this is a list of the files which
    # we will need to read so we need a list to iterate over
    read_list = os.listdir(cfg.my_dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    logger.info('Waiting for input from user')
    input()
    logger.info('Input from user received')

    # here is the loop to iterate through the read_list
    for i in range(len(read_list)):
        print()
        print()
        print("-----------------------------------------------------------------------------------")
        read_file = (cfg.my_dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_index(0)

        # is this actually a timesheet? And which one is it?
        # the timesheets class arguments are as follows
        # (version, name_row, name_column, start_data_row,
        # start_data_col, spaces_per_day)
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            ts11 = TS2011('ts11', 3, 1, 7, 1, 55, 7)
            # r_row = ts11.start_data_row

            print("This 2011 loop was deleted during the python2 to python3 upgrade")
            print("You'll probably want to re-write this 2011 loop someday")

        elif read_sheet.cell_value(14, 0) == 'SUNDAY':
            print("This timesheet belongs to a casual. Begin data scrape")
            ts_cas = TSCasual('ts_cas', 4, 1, 14, 1, 55, 6)
            ts_cas.ts_print_my_name(read_sheet)

            # A loop to iterate through the time slots one at a time
            for r_row in range(ts_cas.start_data_row, ts_cas.end_data_row):
                r_col = ts_cas.start_data_col + 1
                if read_sheet.cell_type(r_row, r_col) != 0:
                    # write shift number
                    data_list = [next_crew_num]
                    next_crew_num += 1

                    cas_hrs = fnc_spinner(read_sheet, r_row, ts_cas,
                                          grab_01_crew_alpha, grab_02_crew_id, grab_03_date,
                                          grab_04_in_time, grab_05_out_time, grab_06_evnt_yr,
                                          grab_07_crew_evnt_id, grab_08_reg, grab_09_ot,
                                          grab_10_dt, grab_11_crew_acct, grab_12_blacks,
                                          grab_13_MP, grab_14_crew_shifttype,
                                          grab_01_crew_alpha1=ts_cas.name_row, grab_01_crew_alpha2=ts_cas.name_column,
                                          grab_02_crew_id1=ts_cas.name_row, grab_02_crew_id2=ts_cas.name_column,
                                          grab_03_date1=3,
                                          grab_04_in_time1=0,
                                          grab_05_out_time1=1,
                                          grab_06_evnt_yr1=3,
                                          grab_07_head_evnt_id1=3,
                                          grab_08_reg1=2,
                                          grab_09_ot1=3,
                                          grab_10_dt1=4,
                                          grab_12_blacks1=5,
                                          grab_13_MP=6)

                    scraped_data_list = [cel for cel in cas_hrs]
                    data_list.extend(scraped_data_list)
                    print(data_list)
                    # add this row to the df
                    print("adding to crew df")
                    my_dict = dict(zip(crew_keys, data_list))
                    df_crew = df_crew.append(my_dict, ignore_index=True)

                else:
                    print("no data in cel B" + str((r_row) + 1))  # move on to the next time slot
                    # TODO: what is this pycharm error above?

        # now we move onto the salaried head loops
        elif read_sheet.cell_value(19, 0) == 'SUNDAY':
            print("This timesheet was designed in 2015. Begin data scrape")
            ts15 = TS2015('ts15', 15, 2, 19, 2, 69, 7)
            ts15.ts_print_my_name(read_sheet)

            # first, lets loop over the 8 hr flags and write those to the list
            r_row = ts15.start_data_row + ts15.spaces_per_day - 1
            while r_row < ts15.end_data_row:
                if read_sheet.cell_value(r_row, 0) == "":
                    r_row+=ts15.spaces_per_day
                else:
                    # write shift number
                    data_list = [next_head_num]
                    next_head_num += 1

                    eight_hr_flg = fnc_spinner(read_sheet, r_row, ts15,
                                               grab_01_head_alpha, grab_02_head_id, grab_03_date,
                                               create_null, create_null, grab_06_evnt_yr,
                                               grab_07_head_evnt_id, create_eight,create_zero, create_zero,
                                               grab_11_head_acct, grab_12_blacks, grab_13_MP,
                                               grab_01_head_alpha1=ts15.name_row, grab_01_head_alpha2=ts15.name_column,
                                               grab_02_head_id1=ts15.name_row, grab_02_head_id2=ts15.name_column,
                                               grab_03_date1=1,
                                               grab_06_evnt_yr1=1,
                                               grab_07_head_evnt_id1=6, grab_07_head_evnt_id2=1,
                                               grab_11_head_acct1=6,
                                               grab_12_blacks1=7,
                                               grab_13_MP=5)

                    scraped_data_list = [cel for cel in eight_hr_flg]
                    data_list.extend(scraped_data_list)
                    print(data_list)
                    # add this row to the df
                    print("adding to head df")
                    my_dict = dict(zip(head_keys, data_list))
                    df_head = df_head.append(my_dict, ignore_index=True)
                    r_row += ts15.spaces_per_day

            # second, lets loop over the stat flags and write those to the list
            r_row = ts15.start_data_row + ts15.spaces_per_day - 4
            while r_row < ts15.end_data_row:
                if read_sheet.cell_value(r_row, 0) == "":
                    r_row+=ts15.spaces_per_day
                else:
                    # write shift number
                    data_list = [next_head_num]
                    next_head_num += 1

                    stat_flg = fnc_spinner(read_sheet, r_row, ts15,
                                               grab_01_head_alpha, grab_02_head_id, grab_03_date,
                                               create_null, create_null, grab_06_evnt_yr,
                                               grab_07_head_evnt_id, create_eight,create_zero, create_zero,
                                               grab_11_head_acct, grab_12_blacks, grab_13_MP,
                                               grab_01_head_alpha1=ts15.name_row, grab_01_head_alpha2=ts15.name_column,
                                               grab_02_head_id1=ts15.name_row, grab_02_head_id2=ts15.name_column,
                                               grab_03_date1=1,
                                               grab_06_evnt_yr1=1,
                                               grab_07_head_evnt_id1=6, grab_07_head_evnt_id2=1,
                                               grab_11_head_acct1=6,
                                               grab_12_blacks1=7,
                                               grab_13_MP=5)

                    scraped_data_list = [cel for cel in stat_flg]
                    data_list.extend(scraped_data_list)
                    print(data_list)
                    # add this row to the df
                    print("adding to head df")
                    my_dict = dict(zip(head_keys, data_list))
                    df_head = df_head.append(my_dict, ignore_index=True)
                    r_row += ts15.spaces_per_day

            # A loop to iterate through the time slots one at a time
            for r_row in range(ts15.start_data_row, ts15.end_data_row):
                # Find the first slot with data
                r_col = ts15.start_data_col

                if read_sheet.cell_type(r_row, r_col) != 0:
                    # write shift number
                    data_list = [next_head_num]
                    next_head_num += 1

                    head_hrs = fnc_spinner(read_sheet, r_row, ts15,
                                           grab_01_head_alpha, grab_02_head_id, grab_03_date,
                                           kris_fix_in, kris_fix_out, grab_06_evnt_yr,
                                           grab_07_head_evnt_id, grab_08_reg, grab_09_ot,
                                           grab_10_dt, grab_11_head_acct, grab_12_blacks,
                                           grab_13_MP,
                                           grab_01_head_alpha1=ts15.name_row, grab_01_head_alpha2=ts15.name_column,
                                           grab_02_head_id1=ts15.name_row, grab_02_head_id2=ts15.name_column,
                                           grab_03_date1=1,
                                           kris_fix_in1=0, kris_fix_in2=ts15.name_row, kris_fix_in3=ts15.name_column,
                                           kris_fix_out1=1, kris_fix_out2=ts15.name_row, kris_fix_out3=ts15.name_column,
                                           grab_06_evnt_yr1=1,
                                           grab_07_head_evnt_id1=6, grab_07_head_evnt_id2=1,
                                           grab_08_reg1=2,
                                           grab_09_ot1=3,
                                           grab_10_dt1=4,
                                           grab_11_head_acct1=6,
                                           grab_12_blacks1=7,
                                           grab_13_MP=5)

                    scraped_data_list = [cel for cel in head_hrs]
                    data_list.extend(scraped_data_list)
                    print(data_list)
                    # add this row to the df
                    print("adding to head df")
                    my_dict = dict(zip(head_keys, data_list))
                    df_head = df_head.append(my_dict, ignore_index=True)


                else:
                    print("no data in cel E" + str((r_row) + 1))  # move on to the next time slot
        print("-----------------------------------------------------------------------------------")
    else:
        print()
        print("We are done")
    print()

    # send the df to the db
    tbl = 'TMPtblWeeklyHeadsData'
    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        tbl_exist = dbfnc.checkTableExists(conn, tbl)

    if tbl_exist:
        with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
            print("let's empty Heads the table")
            cur = conn.cursor()
            cur.execute("DROP Table TMPtblWeeklyHeadsData")

    else:
        print("OOPS! IF YOU ARE READING THIS WE HAVE A PROBLEM!")
        print("NEXT COMES THE ERROR MESSAGE!")

    print("Table path cleared, let's write to the db")
    engine = sa.create_engine(cfg.alc_str)
    df_head.to_sql(tbl,
                   con=engine,
                   if_exists='append',
                   index=False,
                   dtype={'Shift': sa.types.INT,
                          'HeadIDLetter': sa.types.NVARCHAR(length=255),
                          'HeadIDNumber': sa.types.INT,  # notice this is an INT
                          'Date': sa.dialects.mssql.DATETIME2(0),
                          'InTime': sa.dialects.mssql.DATETIME2(0),
                          'OutTime': sa.dialects.mssql.DATETIME2(0),
                          'EventYrID': sa.types.NVARCHAR(length=255),
                          'EventID': sa.types.NVARCHAR(length=255),
                          'Reg': sa.types.FLOAT,
                          'OT': sa.types.FLOAT,
                          'Double': sa.types.FLOAT,
                          'Acct': sa.types.NVARCHAR(length=255),
                          'Blackscall': sa.dialects.mssql.BIT,
                          'MP': sa.dialects.mssql.BIT}
                   )
    print()

    # send the df to the db
    tbl = 'TMPtblWeeklyCrewData'
    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        tbl_exist = dbfnc.checkTableExists(conn, tbl)

    if tbl_exist:
        with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
            print("let's empty the Crew table")
            cur = conn.cursor()
            cur.execute("DROP Table TMPtblWeeklyCrewData")

    else:
        print("OOPS! IF YOU ARE READING THIS WE HAVE A PROBLEM!")
        print("NEXT COMES THE ERROR MESSAGE!")

    print("Table path cleared, let's write to the db")
    engine = sa.create_engine(cfg.alc_str)
    df_crew.to_sql(tbl,
                   con=engine,
                   if_exists='append',
                   index=False,
                   dtype={'Shift': sa.types.INT,
                          'CrewIDLetter': sa.types.NVARCHAR(length=255),
                          'CrewIDNumber': sa.types.NVARCHAR(length=255),  # notice this is a CHAR
                          'Date': sa.dialects.mssql.DATETIME2(0),
                          'InTime': sa.dialects.mssql.DATETIME2(0),
                          'OutTime': sa.dialects.mssql.DATETIME2(0),
                          'EventYrID': sa.types.NVARCHAR(length=255),
                          'EventID': sa.types.NVARCHAR(length=255),
                          'Reg': sa.types.FLOAT,
                          'OT': sa.types.FLOAT,
                          'Double': sa.types.FLOAT,
                          'Acct': sa.types.NVARCHAR(length=255),
                          'Blackscall': sa.dialects.mssql.BIT,
                          'MP': sa.dialects.mssql.BIT,
                          'ShiftType': sa.types.INT}
                   )
    print()
    print("All done! Time to bailout")
    print()



if __name__ == '__main__':
    logger.info('~~~The fiile scrape.py has started~~~')
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("         timesheetscrapper_python3 package launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    logger.info('~~~~The fiile scrape.py has finished OK~~~')
