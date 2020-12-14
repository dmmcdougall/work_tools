"""
This file contains the main function for the timesheet scrapper.  The scrapper
is for taking collected timesheets, scrapping them, and placing that data
into the production database
"""

# imported from standard library
import os
import pandas as pd
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg
import myFunctions as myfnc


def date_grabber(read_sheet,r,c):
    data = read_sheet.cell_value(r, c)
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = year + '-' + month + '-' + day
    return shift_date

def mos_grabber(read_sheet, r,c):
    data = read_sheet.cell_value(r, c)
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    month = f"{shift_date_tuple[1]}"
    return month

def start_time(old):
    new = old.split()
    new2 = new[1].split('-')
    return new2[0]

def end_time(old):
    new = old.split('-')
    return new[1]

def grab_call_type(call):
    data = call.split()
    return data[0]


# and this is the app...
def main():
    # set up the column headers in lists to receive the scraped data
    col_headers = ['month', 'date', 'IN_time',
                   'OUT_time', 'Payee', 'Type',
                   'resource_name', 'description', 'unit_price',
                   'discount', 'adj_price', 'qty',
                   'unit_hrs', 'subtotal', 'gst',
                   'total', 'gl_code']

    # Creating empty dataframes with column names only
    df_cpo_bills = pd.DataFrame(columns=col_headers)

    # create a list of the read_books this is a list of the files which
    # we will need to read so we need a list to iterate over
    read_list = os.listdir(cfg.cpo_bill_dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    input()

    # here is the loop to iterate through the read_list
    for i in range(len(read_list)):
        print()
        print()
        print("-----------------------------------------------------------------------------------")
        read_file = (cfg.cpo_bill_dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_name('Entry Form')

        # A loop to iterate through the time slots one at a time
        # first block starts at A103, last block starts at A1192
        # blocks are 33 rows wide, useful data is 22 rows wide
        r_row = 104
        offset = 22
        while r_row < 1212:
            if (r_row >= i) and (r_row <= i+18):
                if read_sheet.cell_value(r_row, 1)='' and read_sheet.cell_value(r_row, 5)='' and read_sheet.cell_value(r_row, 9)='':
                    r_row +1

                else:
                    cpo_bill_list = []

                    # grab date
                    myfnc.from_func_2_db(cpo_bill_list, date_grabber, read_sheet, r_row -1+offset, 10)

                    # grab month
                    myfnc.from_func_2_db(cpo_bill_list, mos_grabber, read_sheet, r_row -1+offset, 10)

                    # grab start time
                    data = read_sheet.cell_value(r_row - 2 + offset, 0)
                    myfnc.from_func_2_db(cpo_bill_list, start_time, data)

                    # grab end time
                    data = read_sheet.cell_value(r_row -1+offset, 0)
                    myfnc.from_func_2_db(cpo_bill_list, end_time, data)

                    # payee
                    data = "Arts Commons"
                    cpo_bill_list.append(data)

                    # Show Title (type)
                    data = read_sheet.cell_value(0, 0)
                    cpo_bill_list.append(data)

                    # Crew Member (resource_name)
                    data = read_sheet.cell_value(r_row, 0)
                    cpo_bill_list.append(data)

                    # Setup or showcall, etc (description)
                    data = read_sheet.cell_value(r_row-2+offset, 0)
                    myfnc.from_func_2_db(cpo_bill_list, grab_call_type, data)

                    # pay scale (unit_price)
                    if read_sheet.cell_value(r_row, 1) != '':
                        data = read_sheet.cell_value(r_row, 2)
                        cpo_bill_list.append(data)
                    elif read_sheet.cell_value(r_row, 5) != '':
                        data = read_sheet.cell_value(r_row, 6)
                        cpo_bill_list.append(data)
                    else:
                        data = read_sheet.cell_value(r_row, 10)
                        cpo_bill_list.append(data)

                    # discount
                    cpo_bill_list.append('N/A')

                    # adj_price
                    cpo_bill_list.append('N/A')

                    # qty
                    cpo_bill_list.append('N/A')

                    # number of hours (unit_hrs)
                    if read_sheet.cell_value(r_row, 1) != '':
                        data = read_sheet.cell_value(r_row, 1)
                        cpo_bill_list.append(data)
                    elif read_sheet.cell_value(r_row, 5) != '':
                        data = read_sheet.cell_value(r_row, 5)
                        cpo_bill_list.append(data)
                    else:
                        data = read_sheet.cell_value(r_row, 9)
                        cpo_bill_list.append(data)

                    # total hours (subtotal)
                    data = cpo_bill_list[8]*cpo_bill_list[11]
                    cpo_bill_list.append(data)

                    #  gst
                    cpo_bill_list.append(1.00)

                    # total
                    data = cpo_bill_list[12]*cpo_bill_list[13]
                    cpo_bill_list.append(data)

                    # gl_code
                    cpo_bill_list.append('N/A')

                    my_dict = dict(zip(col_headers, cpo_bill_list))
                    df_cpo_bills = df_cpo_bills.append(my_dict, ignore_index=True)

                    r_row + 1
        else:
            i += 18

        print("-----------------------------------------------------------------------------------")
    else:
        print()
        print("We are done")

    print()
    print("All done! Time to save to...")
    print(f"{cfg.cpo_bills_dir}\cpo_bills_records.xls")

    # load the write workbook
    write_book = xlrd.open_workbook(cfg.write_file)
    write_sheet = write_book.sheet_by_index(0)
    new_book = copy(write_book)
    new_sheet = new_book.get_sheet(0)
    new_book.save(f"{cfg.cpo_bills_dir}\cpo_bills_records.xls")
    print("Opening saved file")
    os.system(f"start EXCEL.EXE {cfg.cpo_bills_dir}\cpo_bills_recordsn.xls")
    print()


if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                resco_bill_scraper launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
