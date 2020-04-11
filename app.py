#imported from standard library
import os

#imported from third party repos
import xlrd
from xlutils.copy import copy

#imported from local directories
import config as cfg
import kris_fix as kf
from myClasses import searchDict

def main():

    # load the write workbook
    write_book = xlrd.open_workbook(cfg.write_file)
    write_sheet = write_book.sheet_by_index(0)
    new_book = copy(write_book)
    new_sheet = new_book.get_sheet(0)

    # find first blank cel in write_book and make it the target row
    w_row = write_sheet.nrows
    print(f"{w_row + 1} appears to be the first available row in the write_book.") # write_row is now the write_book row
    print("Does that sound correct? RETURN for yes, CTRL+C for no.")
    input()

    # create a list of the read_books
    read_list = os.listdir(cfg.dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    input()

    # a loop to iterate through the read_list
    i = 0  # file list positiom number
    for i in range(len(read_list)):
        read_file = (cfg.dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_index(0)

        # is this actually a timesheet? And which one is it?
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            timesheet2011()
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

                        # write date
                    if ((r_row >= 19) and (r_row <= 25)):  # SUNDAY
                        data = read_sheet.cell_value(20, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)
                    elif ((r_row >= 26) and (r_row <= 32)):  # MONDAY
                        data = read_sheet.cell_value(27, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)

                    elif ((r_row >= 33) and (r_row <= 39)):  # TUESDAY
                        data = read_sheet.cell_value(34, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)
                    elif ((r_row >= 40) and (r_row <= 46)):  # WEDNESDAY
                        data = read_sheet.cell_value(41, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)
                    elif ((r_row >= 47) and (r_row <= 53)):  # THURSDAY
                        data = read_sheet.cell_value(48, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)
                    elif ((r_row >= 54) and (r_row <= 60)):  # FRIDAY
                        data = read_sheet.cell_value(55, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)
                    elif ((r_row >= 61) and (r_row <= 67)):  # SATURDAY
                        data = read_sheet.cell_value(62, 0)
                        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                        day = "%s" % (shift_date_tuple[2])
                        month = "%s" % (shift_date_tuple[1])
                        year = "%s" % (shift_date_tuple[0])
                        shift_date = day + '/' + month + '/' + year
                        new_sheet.write(w_row, 3, shift_date)
                        print(shift_date)

                    # the kris_fix is done to deal with KL's custom formatting'
                    # kf_format( write row, read row, write sheet, read sheet, read column)

                    # write time in
                    if head_num == 3:  # if it's kris, then...
                        kf.kf_format(w_row,r_row,new_sheet,read_sheet,2)
                    else:  # it's not kris, so....
                        data = read_sheet.cell_value(r_row, 2)
                        if data == '':
                            shift_in_tuple = (0, 0, 0, 0, 0, 0)
                        else:
                            shift_in_tuple = xlrd.xldate_as_tuple(data, 1)
                        if shift_in_tuple[3] < 10:
                            half1_time = "0%s" % (shift_in_tuple[3])
                        else:
                            half1_time = "%s" % (shift_in_tuple[3])
                        if shift_in_tuple[4] == 0:
                            half2_time = "%s0" % (shift_in_tuple[4])
                        else:
                            half2_time = "%s" % (shift_in_tuple[4])
                        time = half1_time + ":" + half2_time
                        print(time)
                        new_sheet.write(w_row, 4, time)

                    # write time out - kris_fix2
                    if head_num == 3:
                        kf.kf_format(w_row, r_row, new_sheet, read_sheet, 3)
                    else:
                        data = read_sheet.cell_value(r_row, 3)
                        if data == '':
                            shift_out_tuple = (0, 0, 0, 0, 0, 0)
                        else:
                            shift_out_tuple = xlrd.xldate_as_tuple(data, 1)
                        if shift_out_tuple[3] < 10:
                            half1_time = "0%s" % (shift_out_tuple[3])
                        else:
                            half1_time = "%s" % (shift_out_tuple[3])
                        if shift_out_tuple[4] == 0:
                            half2_time = "%s0" % (shift_out_tuple[4])
                        else:
                            half2_time = "%s" % (shift_out_tuple[4])
                        time = half1_time + ":" + half2_time
                        print(time)
                        new_sheet.write(w_row, 5, time)

                    # write reg time, ot, dt
                    w_col = 8
                    data = read_sheet.cell_value(r_row, 4)
                    new_sheet.write(w_row, w_col, data)
                    w_col = w_col + 1

                    data = read_sheet.cell_value(r_row, 5)
                    new_sheet.write(w_row, w_col, data)
                    w_col = w_col + 1

                    data = read_sheet.cell_value(r_row, 6)
                    new_sheet.write(w_row, w_col, data)

                    # write accounting code
                    data = read_sheet.cell_value(r_row, 8)
                    print(data)
                    my_dict = searchDict(cfg.acct_codes)
                    for acct_num in my_dict.search_for_match(data):
                        new_sheet.write(w_row, 11, acct_num)

                    # write show data
                    data = 'J'  # this is year specific CHANGE THIS FOR YOUR NEEDS
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
    print()

print()
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("         timesheetscrapper_python3.py file launched")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print()

if __name__ == '__main__':
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()