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
from myClasses import searchDict
import timesheet2011 as tf11
import casualtimesheet as cas

# this method will create the columns in the new .xls sheet
def col_names(col_new_sheet):
    column_names = ["Shift", "HeadIDLetter", "HeadIDNumber",
                    "Date", "InTime", "OutTime",
                    "EventYrID", "EventID", "Reg",
                    "OT", "Double", "Acct",
                    "Blackscall", "MP"]

    for i in range(len(column_names)):
        col_new_sheet.write(0,i, column_names[i])

# this method will write the date to the new .xls sheet
def write_date(dateread_sheet, dater_row, datenew_sheet, datew_row):
    data = dateread_sheet.cell_value(dater_row, 0)
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = day + '/' + month + '/' + year
    datenew_sheet.write(datew_row, 3, shift_date)
    print(shift_date)

# this is a loop, to iterate over the write_date method
def date_loop(read_row, write_row, readsheet2, newsheet2):
    i = 19
    while i < 70:
        if ((read_row >= i) and (read_row <= i + 6)):
            write_date(readsheet2, i + 1, newsheet2, write_row)
            i += 7
        else:
            i += 7

# this method will write the time to the new .xls sheet
def write_time(timeread_sheet, timer_row,timer_col, timenew_sheet, timew_row):
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
    timenew_sheet.write(timew_row, timer_col + 2, time)

# this method will write the hours worked to the new .xls sheet
def write_hrs(hrsread_sheet, hrsr_row, hrsr_col, hrsnew_sheet, hrsw_row, hrsw_col):
    data = hrsread_sheet.cell_value(hrsr_row, hrsr_col)
    hrsnew_sheet.write(hrsw_row, hrsw_col, data)

def main():

    # load the write workbook
    write_book = xlrd.open_workbook(cfg.write_file)
    write_sheet = write_book.sheet_by_index(0)
    new_book = copy(write_book)
    new_sheet = new_book.get_sheet(0)

    # set up the column headers
    col_names(new_sheet)

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
    i = 0  # file list position number
    for i in range(len(read_list)):
        read_file = (cfg.dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_index(0)

        # is this actually a timesheet? And which one is it?
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            tf11.timesheet2011()
        elif read_sheet.cell_value(19, 0) == 'SUNDAY':
            print("This timesheet was designed in 2015. Begin data scrape")

            r_row = 19  # r_row is now the read_book row

            # A loop to iterate through the time slots one at a time
            for r_row in range(19, 68):
                # Find the first slot with data
                if read_sheet.cell_type(r_row, 2) != 0:
                    print("writing data")

                    # write the HeadAlphaID
                    data = 'z'
                    new_sheet.write(w_row, 1, data)

                    # write persons employee number
                    data = read_sheet.cell_value(15, 2)
                    my_dict = searchDict(cfg.dict_heads)
                    for head_num in my_dict.search_for_match(data):
                        new_sheet.write(w_row, 2, head_num)

                    #write date
                    date_loop(r_row, w_row, read_sheet, new_sheet)

                    # write time in
                    if head_num == 3:  # if it's kris, then...
                        kf.kf_format(w_row,r_row,new_sheet,read_sheet,2)
                    else:  # it's not kris, so....
                        write_time(read_sheet, r_row, 2, new_sheet, w_row)

                    # write time out - kris_fix2
                    if head_num == 3:
                        kf.kf_format(w_row, r_row, new_sheet, read_sheet, 3)
                    else:
                        write_time(read_sheet, r_row, 3, new_sheet, w_row)

                    # write reg time, ot, dt
                    w_col = 8
                    write_hrs(read_sheet, r_row, 4, new_sheet, w_row, w_col)
                    w_col = w_col + 1

                    write_hrs(read_sheet, r_row, 5, new_sheet, w_row, w_col)
                    w_col = w_col + 1

                    write_hrs(read_sheet, r_row, 6, new_sheet, w_row, w_col)

                    # write accounting code
                    data = read_sheet.cell_value(r_row, 8)
                    print(data)
                    acct_num = cfg.acct_codes[data]
                    new_sheet.write(w_row, 11, acct_num)

                    # write show data
                    data = 'J'  # this is year specific CHANGE THIS FOR YOUR NEEDS - WRITE SOMETHING BETTER
                    new_sheet.write(w_row, 6, data)

                    data = '0-310820'  # this is year specific
                    if acct_num != '6210-50-504' and acct_num != '6200-50-504':
                        new_sheet.write(w_row, 7, data)
                    # elif acct_num != '6200-50-504':
                    #   new_sheet.write(w_row, 7, data)
                    else:
                        new_sheet.write(w_row, 7, "")

                    # showcall true/false
                    data = read_sheet.cell_value(r_row, 9)
                    if data != '':
                        new_sheet.write(w_row, 12, 1)
                    else:
                        new_sheet.write(w_row, 12, 0)

                    # Meal Penalty true/false
                    data = read_sheet.cell_value(r_row, 7)
                    if data == 1:
                        new_sheet.write(w_row, 13, 1)
                    else:
                        new_sheet.write(w_row, 13, 0)

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