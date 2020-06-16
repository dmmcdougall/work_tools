'''
This file is for taking collected timesheets, scrapping them, and
placing the scraped data into a .xls for further processing.
'''

# imported from standard library
import os

# imported from third party repos
import xlrd
from xlutils.copy import copy

# imported from local directories
import config as cfg
import kris_fix as kf # added when kris broke the scrapper
import myClasses as my_cls
from myClasses import searchDict
import timesheet as ts
from timesheet import ts_2015
from timesheet import ts_2011
from timesheet import ts_casual

# this method will create the columns in the new .xls sheet
def col_names(col_write_sheet):
    column_names = ["Shift", "HeadIDLetter", "HeadIDNumber",
                    "Date", "InTime", "OutTime",
                    "EventYrID", "EventID", "Reg",
                    "OT", "Double", "Acct",
                    "Blackscall", "MP"]

    for i in range(len(column_names)):
        col_write_sheet.write(0,i, column_names[i])

# WHAT DO I NEED WITH THESE METHODS
# READ SHEET, READ ROW, READ COL,
# START ROW, END ROW, START COL END COL
# WRITE SHEET, WRITE ROW, WRITE COL

def write_HeadIDAlpha(headalpha_wsheet, headalpha_wrow, headalpha_wcol):
    data = 'z'
    headalpha_wsheet.write(headalpha_wrow, headalpha_wcol, data)

def grabempNum(empNum_rsheet, empNum_rrow, empNum_rcol):
    data = empNum_rsheet.cell_value(empNum_rrow, empNum_rcol)
    my_dict = searchDict(cfg.dict_heads)
    for head_num in my_dict.search_for_match(data):
        return head_num

def grabempNum2(empNum_rsheet, empNum_rrow, empNum_rcol):
    data = empNum_rsheet.cell_value(empNum_rrow, empNum_rcol)
    mylist = (str.split(data))
    var = mylist[0]
    head_num = cfg.dict_heads[var]
    return head_num

def write_empNum(empNum_rsheet, empNum_rrow, empNum_rcol,emplNum_wsheet, empNum_wrow, emplNum_wcol):
    emplNum_wsheet.write(empNum_wrow, emplNum_wcol, grabempNum(empNum_rsheet, empNum_rrow, empNum_rcol))


# this method will write the date to the new .xls sheet
def write_date(dateread_sheet, dater_row, datewrite_sheet, datew_row):
    data = dateread_sheet.cell_value(dater_row, 0)
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = day + '/' + month + '/' + year
    datewrite_sheet.write(datew_row, 3, shift_date)
    print(shift_date)

def write_date2(wdate_rsheet, wdate_rrow, wdate_rcol, wdate_wsheet, wdate_wrow, wdate_wcol):
    data = wdate_rsheet.cell_value(wdate_rrow, wdate_rcol)
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = year + '-' + month + '-' + day
    print(shift_date)
    wdate_wsheet.write(wdate_wrow, wdate_wcol, shift_date)

# this is a loop, to iterate over the write_date method
def date_loop(loop_func, loop_rsheet, loop_rrow, loop_rcol, loop_wsheet, loop_wrow, loop_wcol):
    i = 19
    while i < 70:
        if ((loop_rrow >= i) and (loop_rrow <= i + 6)):
            loop_func(loop_rsheet, i + 1, loop_rcol, loop_wsheet, loop_wrow, loop_wcol)
            i += 7
        else:
            i += 7

# this method will write the time to the new .xls sheet
def write_time(timeread_sheet, timer_row,timer_col, timewrite_sheet, timew_row):
    data = timeread_sheet.cell_value(timer_row, timer_col)
    if data == '':
        shift_in_tuple = (0, 0, 0, 0, 0, 0)
    else:
        shift_in_tuple = xlrd.xldate_as_tuple(data, 1)
    if shift_in_tuple[3] < 10:
        half1_time = f"{shift_in_tuple[3]}"
    else:
        half1_time = f"{shift_in_tuple[3]}"
    if shift_in_tuple[4] == 0:
        half2_time = f"{shift_in_tuple[4]}0"
    else:
        half2_time = f"{shift_in_tuple[4]}"
    time = half1_time + ":" + half2_time
    print(time)
    timewrite_sheet.write(timew_row, timer_col + 2, time)

# this method will write the hours worked to the new .xls sheet
def write_hrs(hrsread_sheet, hrsr_row, hrsr_col, hrswrite_sheet, hrsw_row, hrsw_col):
    data = hrsread_sheet.cell_value(hrsr_row, hrsr_col)
    hrswrite_sheet.write(hrsw_row, hrsw_col, data)

def grab_acct(grabacct_rsheet, grabacct_rrow, grabacct_rcol):
    acct_num = grabacct_rsheet.cell_value(grabacct_rrow, grabacct_rcol)
    return acct_num

def write_acct(acct_rsheet, acct_rrow, acct_rcol,acct_wsheet, acct_wrow, acct_wcol):
    data = acct_rsheet.cell_value(acct_rrow, acct_rcol)
    print(data)
    acct_wsheet.write(acct_wrow, acct_wcol, grab_acct(acct_rsheet, acct_rrow, acct_rcol))

def grabeventYR2(datestr):
    newdate = str.split(datestr, '/')
    yr_int = int(newdate[2])
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

def writeevntYrID(wvntyr_rsheet, wvntyr_rrow, wvntyr_rcol, wvntyr_wsheet, wvntyr_wrow, wvntyr_wcol):
    data = wvntyr_rsheet.cell_value(wvntyr_rrow, wvntyr_rcol)
    wvntyr_wsheet.write(wvntyr_wrow, wvntyr_wcol, grabeventYR2(data))

def eventid(evnt_rsheet, evnt_rrow, evnt_rcol, evnt_wsheet, evnt_wrow, evnt_wcol):
    data = '0-310820'  # this is year specific
    evnt_num = grab_acct(evnt_rsheet, evnt_rrow, evnt_rcol)
    if evnt_num != '6210-50-504' and evnt_num != '6200-50-504':
        evnt_wsheet.write(evnt_wrow,evnt_wcol, data)
    else:
        evnt_wsheet.write(evnt_wrow, evnt_wcol, "")

def blackscall(blk_rsheet, blk_rrow, blk_rcol, blk_wsheet, blk_wrow, blk_wcol):
    data = blk_rsheet.cell_value(blk_rrow, blk_rcol)
    if data != '':
        blacks = 1
    else:
        blacks = 0

    blk_wsheet.write(blk_wrow, blk_wcol, blacks)
    
def mpcall(mp_rsheet, mp_rrow, mp_rcol, mp_wsheet, mp_wrow, mp_wcol):
    data = mp_rsheet.cell_value(mp_rrow, mp_rcol)
    if data == 1:
        meal = 1
    else:
        meal = 0

    mp_wsheet.write(mp_wrow, mp_wcol, meal)

# Kris changed the formatting of his timesheet to make it more flexible and subsequently
# killed the scrapper.  This is the work around
# this function is for writing the begin and end times of calls

def kf_format(klr_sheet, klr_row, klr_col, klwrite_sheet, klw_row):
    data = klr_sheet.cell_value(klr_row, klr_col)
    kris_str = str(data)
    count_int = len(kris_str)

    if count_int == 1:
        kris_tuple = (0, data, 0, 0)
    elif count_int == 2:
        kris_tuple = (kris_str[0], kris_str[1], 0, 0)
    elif count_int == 3:
        kris_tuple = (0, kris_str[0], kris_str[1], kris_str[2])
    else:
        kris_tuple = (kris_str[0], kris_str[1], kris_str[2], kris_str[3])

    time = str(kris_tuple[0]) + str(kris_tuple[1]) + ":" + str(kris_tuple[2]) + str(kris_tuple[3])
    print(time)
    klwrite_sheet.write(klw_row, klr_col + 2, time)

def main():

    # define timesheets - version, name_row, name_column, start_data_row, start_data_col,
    # end_data_row, space_per_day
    ts15 = ts_2015('ts15', 15, 2, 19, 2, 69, 7)
    ts11 = ts_2011('ts11', 3, 1, 7, 1, 55, 7)
    ts_cas = ts_casual('ts_cas', 9, 1, 14, 1, 55, 6)


    # load the write workbook
    write_book = xlrd.open_workbook(cfg.write_file)
    write_sheet = write_book.sheet_by_index(0)
    new_book = copy(write_book)
    write_sheet = new_book.get_sheet(0)

    # set up the column headers
    col_names(write_sheet)

    #now that the headers are in, set the first write row to be row #2
    w_row = 1
    print(f"Row number {w_row + 1} appears to be the first available row in the write_book.")
    print("Does that sound correct? RETURN for yes, CTRL+C for no.")
    input()

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

        #WHAT DO I NEED WITH THESE METHODS
        # READ SHEET, READ ROW, READ COL, START ROW, END ROW, START COL END COL
        # WRITE SHEET, WRITE ROW, WRITE COL

        # is this actually a timesheet? And which one is it?
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            tf11.timesheet2011()
        elif read_sheet.cell_value(19, 0) == 'SUNDAY':
            print("This timesheet was designed in 2015. Begin data scrape")

            #r_row = 19  # r_row is now the read_book row
            r_row = ts15.start_data_row

            # A loop to iterate through the time slots one at a time
            for r_row in range(19, 68):
                # Find the first slot with data
                if read_sheet.cell_type(r_row, 2) != 0:
                    print("writing data")

                    # write the HeadAlphaID
                    w_col = 1
                    write_sheet.write(w_row, w_col,ts.timesheet.ts_grabHeadIDAlpha(ts15, read_sheet))

                    # write head employee number
                    w_col = 2
                    write_sheet.write(w_row,w_col,ts.timesheet.ts_grabempNum(ts15, read_sheet))

                    #write date
                    r_col =0
                    w_col = 3
                    i = 19
                    while i < 70:
                        if ((r_row >= i) and (r_row <= i + 6)):
                            ts.ts_2015(ts15, read_sheet, i + 1, r_col, write_sheet, w_row, w_col)
                            i += 7
                        else:
                            i += 7

                    # ts.timesheet.ts_date_loop(date_loop(
                    #     ts15, read_sheet, r_row, r_col, write_sheet, w_row, w_col),
                    #     read_sheet, r_row, r_col, write_sheet, w_row, w_col)

                    # write time in
                    r_col = 2
                    if grabempNum2(read_sheet,15,2) == 3:  # if it's kris, then...
                        kf_format(read_sheet, r_row, 2, write_sheet,w_row)
                    else:  # it's not kris, so....
                        write_time(read_sheet, r_row, 2, write_sheet, w_row)

                    # write time out - kris_fix2
                    if grabempNum2(read_sheet,15,2) == 3:
                        kf_format(read_sheet, r_row, 2, write_sheet,w_row)
                    else:
                        write_time(read_sheet, r_row, 3, write_sheet, w_row)

                    # write reg time, ot, dt
                    w_col = 8
                    write_hrs(read_sheet, r_row, 4, write_sheet, w_row, w_col)
                    w_col = w_col + 1

                    write_hrs(read_sheet, r_row, 5, write_sheet, w_row, w_col)
                    w_col = w_col + 1

                    write_hrs(read_sheet, r_row, 6, write_sheet, w_row, w_col)

                    # write accounting code
                    r_col = 8
                    w_col = 11
                    write_acct(read_sheet, r_row, r_col, write_sheet, w_row, w_col)

                    # data = read_sheet.cell_value(r_row, 8)
                    # print(data)
                    # acct_num = cfg.acct_codes[data]
                    # write_sheet.write(w_row, 11, acct_num)

                    # write show data
                    w_col = 6
                    data = 'J'  # this is year specific CHANGE THIS FOR YOUR NEEDS - WRITE SOMETHING BETTER
                    write_sheet.write(w_row, w_col, data)

                    # w_col = 6
                    # date_loop(writeevntYrID, read_sheet, r_row, r_col, write_sheet,w_row, w_col)

                    # show id
                    w_col = 7
                    eventid(read_sheet, r_row, r_col, write_sheet, w_row, w_col)

                    # showcall true/false
                    r_col=9
                    w_col = 12

                    blackscall(read_sheet, r_row, r_col, write_sheet, w_row, w_col)

                    # Meal Penalty true/false
                    r_col = 7
                    w_col = 13
                    mpcall(read_sheet, r_row, r_col, write_sheet, w_row, w_col)

                    w_row = w_row + 1  # move along in the write_book

                else:
                    print("no data in cel E" + str((r_row) + 1))  # move on to the next time slot

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