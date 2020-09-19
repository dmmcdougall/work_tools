"""
This file is for taking collected timesheets, scrapping them, and....
"""

# imported from standard library
import os
import pandas as pd

# imported from third party repos
import xlrd

# imported from local directories
import config as cfg
import databaseFunctions as dbfnc
import kris_fix as kf # added when kris broke the scrapper
import myClasses as my_cls
from myClasses import searchDict
from timesheet import ts_2015
from timesheet import ts_2011
from timesheet import ts_casual

#
# def grab_acct(grabacct_rsheet, grabacct_rrow, grabacct_rcol):
#     acct_num = grabacct_rsheet.cell_value(grabacct_rrow, grabacct_rcol)
#     return acct_num
#
# def write_acct(acct_rsheet, acct_rrow, acct_rcol,acct_wsheet, acct_wrow, acct_wcol):
#     data = acct_rsheet.cell_value(acct_rrow, acct_rcol)
#     print(data)
#     acct_wsheet.write(acct_wrow, acct_wcol, grab_acct(acct_rsheet, acct_rrow, acct_rcol))

# def eventid(evnt_rsheet, evnt_rrow, evnt_rcol, evnt_wsheet, evnt_wrow, evnt_wcol):
#     data = '0-310820'  # this is year specific
#     evnt_num = grab_acct(evnt_rsheet, evnt_rrow, evnt_rcol)
#     if evnt_num != '6210-50-504' and evnt_num != '6200-50-504':
#         evnt_wsheet.write(evnt_wrow,evnt_wcol, data)
#     else:
#         evnt_wsheet.write(evnt_wrow, evnt_wcol, "")
#
# def blackscall(blk_rsheet, blk_rrow, blk_rcol, blk_wsheet, blk_wrow, blk_wcol):
#     data = blk_rsheet.cell_value(blk_rrow, blk_rcol)
#     if data != '':
#         blacks = 1
#     else:
#         blacks = 0
#
#     blk_wsheet.write(blk_wrow, blk_wcol, blacks)
#
# def mpcall(mp_rsheet, mp_rrow, mp_rcol, mp_wsheet, mp_wrow, mp_wcol):
#     data = mp_rsheet.cell_value(mp_rrow, mp_rcol)
#     if data == 1:
#         meal = 1
#     else:
#         meal = 0
#
#     mp_wsheet.write(mp_wrow, mp_wcol, meal)
#
# # Kris changed the formatting of his timesheet to make it more flexible and subsequently
# # killed the scrapper.  This is the work around
# # this function is for writing the begin and end times of calls
#
# def kf_format(klr_sheet, klr_row, klr_col, klwrite_sheet, klw_row):
#     data = klr_sheet.cell_value(klr_row, klr_col)
#     kris_str = str(data)
#     count_int = len(kris_str)
#
#     if count_int == 1:
#         kris_tuple = (0, data, 0, 0)
#     elif count_int == 2:
#         kris_tuple = (kris_str[0], kris_str[1], 0, 0)
#     elif count_int == 3:
#         kris_tuple = (0, kris_str[0], kris_str[1], kris_str[2])
#     else:
#         kris_tuple = (kris_str[0], kris_str[1], kris_str[2], kris_str[3])
#
#     time = str(kris_tuple[0]) + str(kris_tuple[1]) + ":" + str(kris_tuple[2]) + str(kris_tuple[3])
#     print(time)
#     klwrite_sheet.write(klw_row, klr_col + 2, time)

def main():
    # set up the column headers
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

    # find the max number in the Shift number lists
    query = "SELECT * FROM HeadShiftWorkedTable"
    df_hShift = pd.read_sql(query, cfg.conn)
    head_record = df_hShift['HeadShiftWorkedID'].max()
    next_head_num = head_record +1

    query = "SELECT * FROM CrewShiftWorkedTable"
    df_hShift = pd.read_sql(query, cfg.conn)
    crew_record = df_hShift['ShiftWorkedID'].max()
    next_crew_num = crew_record + 1

    # create a list of the read_books
    read_list = os.listdir(cfg.dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    input()

    # a loop to iterate through the read_list
    i = 0  # where in the list are we?
    for i in range(len(read_list)):
        read_file = (cfg.dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_index(0)

        # is this actually a timesheet? And which one is it?
        # define timesheets - version, name_row, name_column, start_data_row,
        # start_data_col, spaces_per_day
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            ts11 = ts_2011('ts11', 3, 1, 7, 1, 55, 7)
            r_row = ts11.start_data_row

        elif read_sheet.cell_value(14, 0) == 'SUNDAY':
            print("This timesheet belongs to a casual. Begin data scrape")
            ts_cas = ts_casual('ts_cas', 9, 1, 14, 1, 55, 6)
            r_row = ts_cas.start_data_row

            # A loop to iterate through the time slots one at a time
            for r_row in range(ts_cas.start_data_row, ts_cas.end_data_row):
                if read_sheet.cell_type(r_row, 2) != 0:
                    print("writing data")

                    # House keeping...
                    # create an empty list to store the data and increment the shift number
                    crew_data_list = []

                    # write shift number
                    crew_data_list.append(next_crew_num)
                    next_crew_num +=1

                    # Grab a casual Alpha number from the db
                    data = read_sheet.cell_value(9,1)
                    casAlpha_id = dbfnc.find_crew_Alpha_number(data)
                    print(casAlpha_id)
                    crew_data_list.append(casAlpha_id)

                    # Grab a casual number from the db
                    data = read_sheet.cell_value(9,1)
                    cas_id = dbfnc.find_crew_number(data)
                    print(cas_id)
                    crew_data_list.append(cas_id)

                    # Grab ts date
                    data = ts_cas.ts_grabdate(read_sheet,r_row)
                    print(data)
                    crew_data_list.append(data)

                    # Grab in time
                    r_col = ts_cas.start_data_col
                    data = ts_cas.ts_write_time(read_sheet,r_row, r_col)
                    print(data)
                    crew_data_list.append(data)

                    # Grab out time
                    r_col = ts_cas.start_data_col+1
                    data = ts_cas.ts_write_time(read_sheet,r_row, r_col)
                    print(data)
                    crew_data_list.append(data)

                    # Grab event year
                    data = ts_cas.ts_grabdate(read_sheet,r_row)
                    print(data + " prepped date")
                    evntYr = dbfnc.grabeventYR2(data)
                    crew_data_list.append(evntYr)

                    # Grab Event ID
                    data = ts_cas.ts_grabdate(read_sheet, r_row)
                    show = ts_cas.tscas_write_show_num(data)
                    crew_data_list.append(show)

                    # write reg time, ot, dt
                    r_col = ts_cas.start_data_col+2
                    data = ts_cas.ts_grabhrs(read_sheet,r_row,r_col)
                    crew_data_list.append(data)
                    r_col = r_col + 1

                    data = ts_cas.ts_grabhrs(read_sheet, r_row, r_col)
                    crew_data_list.append(data)
                    r_col = r_col + 1

                    data = ts_cas.ts_grabhrs(read_sheet, r_row, r_col)
                    crew_data_list.append(data)

                    # write accounting code
                    data = ts_cas.tscas_write_acct()
                    crew_data_list.append(data)

                    # showcall true/false
                    r_col = ts_cas.start_data_col+5
                    data = ts_cas.ts_blacks_call(r_row,r_col)
                    crew_data_list.append(data)

                    print(crew_data_list)

                    # Grab MP
                    r_col = ts_cas.start_data_col+6
                    data = ts_cas.ts_mp(r_row,r_col)
                    crew_data_list.append(data)

                    # Grab Shiftype
                    data = ts_cas.tscas_write_shifttype()
                    crew_data_list.append(data)

                    print("adding to crew df")

                    df_crew = pd.DataFrame(crew_data_list, columns=crew_keys)

                else:
                    print("no data in cel B" + str((r_row) + 1))  # move on to the next time slot

        # elif read_sheet.cell_value(19, 0) == 'SUNDAY':
        #     print("This timesheet was designed in 2015. Begin data scrape")
        #     ts15 = ts_2015('ts15', 15, 2, 19, 2, 69, 7)
        #     r_row = 19  # r_row is now the read_book row
        #     r_row = ts15.start_data_row
        #
        #     # A loop to iterate through the time slots one at a time
        #     for r_row in range(19, 68):
        #         # Find the first slot with data
        #         if read_sheet.cell_type(r_row, 2) != 0:
        #             print("writing data")
        #
        #             # write the HeadAlphaID
        #             w_col = 1
        #             write_sheet.write(w_row, w_col,ts.timesheet.ts_grabHeadIDAlpha(ts15, read_sheet))
        #
        #             # write head employee number
        #             w_col = 2
        #             write_sheet.write(w_row,w_col,ts.timesheet.ts_grabempNum(ts15, read_sheet))
        #
        #             #write date
        #             r_col =0
        #             w_col = 3
        #             i = 19
        #             while i < 70:
        #                 if ((r_row >= i) and (r_row <= i + 6)):
        #                     ts.ts_2015(ts15, read_sheet, i + 1, r_col, write_sheet, w_row, w_col)
        #                     i += 7
        #                 else:
        #                     i += 7
        #
        #             # ts.timesheet.ts_date_loop(date_loop(
        #             #     ts15, read_sheet, r_row, r_col, write_sheet, w_row, w_col),
        #             #     read_sheet, r_row, r_col, write_sheet, w_row, w_col)
        #
        #             # write time in
        #             r_col = 2
        #             if grabempNum2(read_sheet,15,2) == 3:  # if it's kris, then...
        #                 kf_format(read_sheet, r_row, 2, write_sheet,w_row)
        #             else:  # it's not kris, so....
        #                 write_time(read_sheet, r_row, 2, write_sheet, w_row)
        #
        #             # write time out - kris_fix2
        #             if grabempNum2(read_sheet,15,2) == 3:
        #                 kf_format(read_sheet, r_row, 2, write_sheet,w_row)
        #             else:
        #                 write_time(read_sheet, r_row, 3, write_sheet, w_row)
        #
        #             # write reg time, ot, dt
        #             w_col = 8
        #             write_hrs(read_sheet, r_row, 4, write_sheet, w_row, w_col)
        #             w_col = w_col + 1
        #
        #             write_hrs(read_sheet, r_row, 5, write_sheet, w_row, w_col)
        #             w_col = w_col + 1
        #
        #             write_hrs(read_sheet, r_row, 6, write_sheet, w_row, w_col)
        #
        #             # write accounting code
        #             r_col = 8
        #             w_col = 11
        #             write_acct(read_sheet, r_row, r_col, write_sheet, w_row, w_col)
        #
        #             # data = read_sheet.cell_value(r_row, 8)
        #             # print(data)
        #             # acct_num = cfg.acct_codes[data]
        #             # write_sheet.write(w_row, 11, acct_num)
        #
        #             # write show data
        #             w_col = 6
        #             data = 'J'  # this is year specific CHANGE THIS FOR YOUR NEEDS - WRITE SOMETHING BETTER
        #             write_sheet.write(w_row, w_col, data)
        #
        #             # w_col = 6
        #             # date_loop(writeevntYrID, read_sheet, r_row, r_col, write_sheet,w_row, w_col)
        #
        #             # show id
        #             w_col = 7
        #             eventid(read_sheet, r_row, r_col, write_sheet, w_row, w_col)
        #
        #             # showcall true/false
        #             r_col=9
        #             w_col = 12
        #
        #             blackscall(read_sheet, r_row, r_col, write_sheet, w_row, w_col)
        #
        #             # Meal Penalty true/false
        #             r_col = 7
        #             w_col = 13
        #             mpcall(read_sheet, r_row, r_col, write_sheet, w_row, w_col)
        #
        #             w_row = w_row + 1  # move along in the write_book
        #
        #         else:
        #             print("no data in cel E" + str((r_row) + 1))  # move on to the next time slot

    else: print("this is NOT a timesheet")
    print()
    print("All done! Time to save to...")
    print(f"{cfg.home}\Desktop\scraped_by_python.xls")
    new_book.save(f"{cfg.home}\Desktop\scraped_by_python.xls")
    # putting a hold on these two lines while I work on the post2db.py
    # print("Opening saved file")
    # os.system(f"start EXCEL.EXE {cfg.home}\Desktop\scraped_by_python.xls")
    print()

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("         timesheetscrapper_python3.py file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()