"""
This file contains the main function for the timesheet scrapper.  The scrapper
is for taking collected timesheets, scrapping them, and placing that data
into the production database
"""

# imported from standard library
import os
import logging
import pandas as pd
import xlrd
from xlutils.copy import copy

# imported from third party repos

# imported from local directories
import config as cfg
import myFunctions as myfnc

# logging info
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # change to DEBUG when required

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(cfg.log_files + '\\' + 'resco_bill_scrape.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def date_grabber(read_sheet,r,c):
    data = read_sheet.cell_value(r, c)
    # logger.info(f'the date_grabber has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    # logger.info(f'the date_grabber has turned it into {shift_date_tuple}')
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = year + '-' + month + '-' + day
    return shift_date

def mos_grabber(read_sheet, r,c):
    data = read_sheet.cell_value(r, c)
    logger.info(f'the mos_grabber has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    logger.info(f'the mos_grabber has turned it into {shift_date_tuple}')
    month = f"{shift_date_tuple[1]}"
    return month

def start_time(old):
    logger.info(f'the start_time has grabbed {old} to parse')
    new = old.split()
    new2 = new[1].split('-')
    logger.info(f'the start_time has turned it into {new2}')
    return new2[0]

def end_time(old):
    logger.info(f'the end_time has grabbed {old} to parse')
    new = old.split('-')
    logger.info(f'the end_time has turned it into {new}')
    return new[1]

def grab_call_type(call):
    logger.info(f'the grab_call_type has grabbed {call} to parse')
    data = call.split()
    logger.info(f'the grab_call_type has turned it into {data}')
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
        logger.debug("")
        logger.debug("-----------------------------------------------------------------------------------")
        read_file = (cfg.cpo_bill_dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_name('Entry Form')

        # A loop to iterate through the time slots one at a time
        # first block starts at A103, last block starts at A1192
        # blocks are 33 rows wide, useful data is 22 rows wide

        # offset = 0
        loop = 0
        start_r_row = 104

        # this loop is the call block
        first_loop = 0
        info_block = 102

        for first_loop in range(33):
            # info_block = first loop + start_info_block
            logger.debug("")
            logger.debug(f'**NEW CALL** info_block = {info_block}')
            if read_sheet.cell_value(info_block, 0) == 'CALL':
                break
            else:
                for loop in range(18):
                    # reg loop
                    r_row = start_r_row+loop
                    reg = read_sheet.cell_value(r_row, 1)

                    if reg != '':
                        logger.debug(f'r_row = {r_row}')
                        logger.debug(f'reg = {reg}')
                        cpo_bill_list = []

                        # grab date
                        myfnc.from_func_2_db(cpo_bill_list, date_grabber, read_sheet, info_block +1, 0)

                        # grab month
                        myfnc.from_func_2_db(cpo_bill_list, mos_grabber, read_sheet, info_block +1 , 0)

                        # grab start time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
                            myfnc.from_func_2_db(cpo_bill_list, start_time, data)

                        # grab end time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
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
                        data = read_sheet.cell_value(info_block, 0)
                        myfnc.from_func_2_db(cpo_bill_list, grab_call_type, data)

                        # pay scale (unit_price)
                        data = read_sheet.cell_value(r_row, 2)
                        cpo_bill_list.append(data)

                        # discount
                        cpo_bill_list.append('N/A')

                        # adj_price
                        cpo_bill_list.append('N/A')

                        # qty
                        cpo_bill_list.append('N/A')

                        # number of hours (unit_hrs)
                        data = read_sheet.cell_value(r_row, 1)
                        cpo_bill_list.append(data)

                        # total hours (subtotal)
                        logger.info(f'the list has {cpo_bill_list[8]} and {cpo_bill_list[12]} to multiple')
                        data = cpo_bill_list[8]*cpo_bill_list[12]
                        cpo_bill_list.append(data)

                        #  gst
                        cpo_bill_list.append(1.00)

                        # total
                        data = cpo_bill_list[13]*cpo_bill_list[14]
                        cpo_bill_list.append(data)

                        # gl_code
                        cpo_bill_list.append('N/A')

                        print(cpo_bill_list)

                        my_dict = dict(zip(col_headers, cpo_bill_list))
                        df_cpo_bills = df_cpo_bills.append(my_dict, ignore_index=True)

                        r_row += 1

                    else:
                        r_row += 1

                r_row = 104
                for i in range(18):
                    # ot loop
                    ot = read_sheet.cell_value(r_row, 5)
                    if ot != '':
                        logger.debug(f'r_row = {r_row}')
                        logger.debug(f'ot = {ot}')
                        cpo_bill_list = []

                        # grab date
                        myfnc.from_func_2_db(cpo_bill_list, date_grabber, read_sheet, info_block + 1, 0)

                        # grab month
                        myfnc.from_func_2_db(cpo_bill_list, mos_grabber, read_sheet, info_block + 1, 0)

                        # grab start time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
                            myfnc.from_func_2_db(cpo_bill_list, start_time, data)

                        # grab end time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
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
                        data = read_sheet.cell_value(info_block, 0)
                        myfnc.from_func_2_db(cpo_bill_list, grab_call_type, data)

                        # pay scale (unit_price)
                        data = read_sheet.cell_value(r_row, 6)
                        cpo_bill_list.append(data)

                        # discount
                        cpo_bill_list.append('N/A')

                        # adj_price
                        cpo_bill_list.append('N/A')

                        # qty
                        cpo_bill_list.append('N/A')

                        # number of hours (unit_hrs)
                        data = read_sheet.cell_value(r_row, 5)
                        cpo_bill_list.append(data)

                        # total hours (subtotal)
                        logger.info(f'the list has {cpo_bill_list[8]} and {cpo_bill_list[12]} to multiply')
                        data = cpo_bill_list[8] * cpo_bill_list[12]
                        cpo_bill_list.append(data)

                        #  gst
                        cpo_bill_list.append(1.00)

                        # total
                        data = cpo_bill_list[13] * cpo_bill_list[14]
                        cpo_bill_list.append(data)

                        # gl_code
                        cpo_bill_list.append('N/A')

                        print(cpo_bill_list)

                        my_dict = dict(zip(col_headers, cpo_bill_list))
                        df_cpo_bills = df_cpo_bills.append(my_dict, ignore_index=True)

                        r_row += 1

                    else:
                        r_row += 1

                r_row = 104
                for i in range(18):
                    # dt loop
                    dt = read_sheet.cell_value(r_row, 9)
                    if dt != '':
                        logger.debug(f'r-row = {r_row}')
                        logger.debug(f'dt = {dt}')
                        cpo_bill_list = []

                        # grab date
                        myfnc.from_func_2_db(cpo_bill_list, date_grabber, read_sheet, info_block + 1, 0)

                        # grab month
                        myfnc.from_func_2_db(cpo_bill_list, mos_grabber, read_sheet, info_block + 1, 0)

                        # grab start time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
                            myfnc.from_func_2_db(cpo_bill_list, start_time, data)

                        # grab end time
                        if read_sheet.cell_value(info_block, 0) == 'Strike':
                            cpo_bill_list.append('Strike')
                        else:
                            data = read_sheet.cell_value(info_block, 0)
                            myfnc.from_func_2_db(cpo_bill_list, end_time, data)

                        # payee
                        data = "Arts Commons"
                        cpo_bill_list.append(data)

                        # Show Title (type)
                        data = read_sheet.cell_value(0, 0)
                        cpo_bill_list.append(data)

                        # Crew Member (resource_name)
                        data = read_sheet.cell_value(r_row, 0)

                        # Setup or showcall, etc (description)
                        data = read_sheet.cell_value(info_block, 0)
                        myfnc.from_func_2_db(cpo_bill_list, grab_call_type, data)

                        cpo_bill_list.append(data)

                        # pay scale (unit_price)
                        data = read_sheet.cell_value(r_row, 10)
                        cpo_bill_list.append(data)

                        # discount
                        cpo_bill_list.append('N/A')

                        # adj_price
                        cpo_bill_list.append('N/A')

                        # qty
                        cpo_bill_list.append('N/A')

                        # number of hours (unit_hrs)
                        data = read_sheet.cell_value(r_row, 9)
                        cpo_bill_list.append(data)

                        # total hours (subtotal)
                        logger.info(f'the list has {cpo_bill_list[8]} and {cpo_bill_list[12]} to multiple')
                        data = cpo_bill_list[8] * cpo_bill_list[12]
                        cpo_bill_list.append(data)

                        #  gst
                        cpo_bill_list.append(1.00)

                        # total
                        data = cpo_bill_list[13] * cpo_bill_list[14]
                        cpo_bill_list.append(data)

                        # gl_code
                        cpo_bill_list.append('N/A')

                        print(cpo_bill_list)

                        my_dict = dict(zip(col_headers, cpo_bill_list))
                        df_cpo_bills = df_cpo_bills.append(my_dict, ignore_index=True)

                        r_row += 1

                    else:
                        r_row += 1

            info_block+=33

        print("-----------------------------------------------------------------------------------")
    else:
        print()
        print("We are done")

    print()
    print("All done! Time to save to...")
    print(f"{cfg.desktop_dir}\cpo_bills_records.xls")

    df_cpo_bills.to_excel(f'{cfg.desktop_dir}\cpo_bills_records.xlsx', index=False)


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
