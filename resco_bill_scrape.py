"""
This file scrapes all the data from a bill and formats it into
a timesheet as defined by a resco
"""

# imported from standard library
import logging
import os
import pandas as pd
import xlrd

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

# TODO: refactor the fuck out of this trash heap

# this loop goes along a row of data and scrapes the data using the appropriate function
def bill_row_scrapper(read_sheet, info_block, r_row, col, *args):
    for i in range(len(args)):
        func = args[i]
        function_name = func.__name__
        yield func(read_sheet, info_block, r_row, col)

# grab the month - this first one grabs from the info block
def resco_0_mos(read_sheet, info_block, dummy2, dummy3):
    data = read_sheet.cell_value(info_block+1, 0)
    logger.info(f'the resco_0_mos has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    logger.info(f'the resco_0_mos has turned it into {shift_date_tuple}')
    month = f"{shift_date_tuple[1]}"
    return month

# this one grabs from the date in the header.  good for prep time and inventory items
def resco_0b_mos(read_sheet, dummy1, dummy2, dummy3):
    data = read_sheet.cell_value(0, 10)
    logger.info(f'the resco_0b_mos has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    logger.info(f'the resco_0b_mos has turned it into {shift_date_tuple}')
    month = f"{shift_date_tuple[1]}"
    return month

# grab the date - this first one grabs from the info block
def resco_1_date(read_sheet, info_block, dummy2, dummy3):
    data = read_sheet.cell_value(info_block+1, 0)
    # logger.info(f'the date_grabber has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    # logger.info(f'the date_grabber has turned it into {shift_date_tuple}')
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = month + '-' + day + '-' + year
    return shift_date

# this one grabs from the date in the header.  good for prep time and inventory items
def resco_1b_date(read_sheet, dummy1, dummy2, dummy3):
    data = read_sheet.cell_value(0, 10)
    # logger.info(f'the date_grabber has grabbed {data} to parse')
    shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
    # logger.info(f'the date_grabber has turned it into {shift_date_tuple}')
    day = f"{shift_date_tuple[2]}"
    month = f"{shift_date_tuple[1]}"
    year = f"{shift_date_tuple[0]}"
    shift_date = month + '-' + day + '-' + year
    return shift_date

# grab the in time of a labour call
def resco_2_IN(read_sheet, info_block, dummy2, dummy3):
    data = read_sheet.cell_value(info_block, 0)
    if data == 'Strike':
        return data
    else:
        #logger.info(f'the start_time has grabbed {old} to parse')
        data = read_sheet.cell_value(info_block, 0)
        new = data.split('-')
        new2 = new[0].split()
        # logger.info(f'the start_time has turned it into {new2}')
        return new2[-1]

# grab the out time of a labour call
def resco_3_OUT(read_sheet, info_block, dummy2, dummy3):
    data = read_sheet.cell_value(info_block, 0)
    if data == 'Strike':
        return data
    else:
        # logger.info(f'the end_time has grabbed {old} to parse')
        new = data.rsplit('-')
        # logger.info(f'the end_time has turned it into {new}')
        return new[1]

# create a payee
def resco_4_payee(dummy, dummy1, dummy2, dummy3):
    data = "Arts Commons"
    return data

# what type of call is it Setup, Strike...- this first one grabs from the info block
def resco_5_type(read_sheet, info_block, dummy2, dummy3):
    data = read_sheet.cell_value(info_block, 0)
    logger.info(f'the grab_call_type has grabbed {data} to parse')
    call = data.rsplit(' ', 1)
    logger.info(f'the grab_call_type has turned it into {call}')
    return call[0]

# this one is only for the preptime loop
def resco_5b_type(dummy, dummy1, dummy2, dummy3):
    data = "PREP TIME"
    return data

# who is it, FULLTIME< CASUAUL etc...
def resco_6_resource(read_sheet, dummy1, row, dummy3):
    data = read_sheet.cell_value(row, 0)
    return data

# resource for an MP
def resco_6b_resource(dummy, dummy1, dummy2, dummy3):
    data = "Meal Penalty"
    return data

# project title
def resco_7_description(read_sheet, dummy1, dummy2, dummy3):
    data = read_sheet.cell_value(0, 0)
    return data

# grab cost per hour/unit
def resco_8_unitprice(read_sheet, dummy1,row, col):
    data = read_sheet.cell_value(row, col)
    return data

# 9, 10, 11 is null

# this quantity is MP only
def resco_11b_qty(read_sheet, dummy1, row, col):
    data = read_sheet.cell_value(row, col)
    return data

# grab the number of hours worked
def resco_12_hrs(read_sheet, dummy1, row, col):
    data = read_sheet.cell_value(row, col)
    return data

# subtotal = unit hrs * rate
def resco_13_subtotal(read_sheet, dummy1, row, col):
    hrs_qty = read_sheet.cell_value(row, col)
    rate_price = read_sheet.cell_value(row, col + 1)
    return hrs_qty * rate_price

# 14 is NULL

# total = unit hrs * rate
def resco_15_total(read_sheet, dummy1,row, col):
    hrs_qty = read_sheet.cell_value(row, col)
    rate_price = read_sheet.cell_value(row, col +1)
    return hrs_qty*rate_price

# insert a NULL value
def resco_x_NULL(dummy, dummy1, dummy2, dummy3):
    data = ""
    return data


# and this is the app...
def main():
    # set up the column headers in lists to receive the scraped data
    col_headers = ['month', 'date', 'IN_time',
                   'OUT_time', 'Payee', 'Type',
                   'resource_name', 'description', 'unit_price',
                   'discount', 'adj_price', 'qty',
                   'unit_hrs', 'subtotal', 'gst',
                   'total']

    # these are required for the labour_loop
    dummy, dummy1, dummy2, dummy3 = 0, 0, 0, 0

    # Creating empty dataframes with column names only
    df_bill_data = pd.DataFrame(columns=col_headers)

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
        print("------------------------------------------------------------------------------------------------")
        logger.debug("")
        logger.debug("------------------------------------------------------------------------------------------------")
        read_file = (cfg.cpo_bill_dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_name('Entry Form')

        # the prep time grab
        # reg time
        logger.debug(f"Entering Prep Time Reg")
        r_row = 95
        col = 1
        for i in range(2):
            logger.debug(f"r_row Now = {r_row}")
            units = read_sheet.cell_value(r_row, col)
            if units !='':
                prep_time_reg = bill_row_scrapper(read_sheet, dummy, r_row, col,
                                           resco_0b_mos, resco_1b_date, resco_x_NULL,
                                           resco_x_NULL, resco_4_payee, resco_5b_type,
                                           resco_6_resource, resco_7_description, resco_8_unitprice,
                                           resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                           resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                           resco_15_total)

                row_data_list = [cel for cel in prep_time_reg]
                print(row_data_list)

                my_dict = dict(zip(col_headers, row_data_list))
                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

                r_row += 1

            else:
                r_row += 1

        # this loop covers the first two ot rows, FULLTIME and CASUAL
        logger.debug(f"Entering Prep Time OT")
        r_row = 95
        for i in range(2):
            logger.debug(f"r_row Now = {r_row}")
            col = 5 # this is the location of the ot time data
            units = read_sheet.cell_value(r_row, col)
            if units !='':
                prep_time_ot = bill_row_scrapper(read_sheet, dummy, r_row, col,
                                          resco_0b_mos, resco_1b_date, resco_x_NULL,
                                          resco_x_NULL, resco_4_payee, resco_5b_type,
                                          resco_6_resource, resco_7_description, resco_8_unitprice,
                                          resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                          resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                          resco_15_total)

                row_data_list = [cel for cel in prep_time_ot]
                print(row_data_list)

                my_dict = dict(zip(col_headers, row_data_list))
                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

                r_row += 1

            else:
                r_row += 1

        # this loop covers the first two dt rows, FULLTIME and CASUAL
        logger.debug(f"Entering Prep Time DT")
        r_row = 95
        for i in range(2):
            logger.debug(f"r_row Now = {r_row}")
            col = 9 # this is the location of the dt time data
            units = read_sheet.cell_value(r_row, col)
            if units !='':
                prep_time_dt = bill_row_scrapper(read_sheet, dummy, r_row, col,
                                          resco_0b_mos, resco_1b_date, resco_x_NULL,
                                          resco_x_NULL, resco_4_payee, resco_5b_type,
                                          resco_6_resource, resco_7_description, resco_8_unitprice,
                                          resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                          resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                          resco_15_total)

                row_data_list = [cel for cel in prep_time_dt]
                print(row_data_list)

                my_dict = dict(zip(col_headers, row_data_list))
                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

                r_row += 1

            else:
                r_row += 1
                
        # MP
        logger.debug(f"Entering MP")
        r_row = 60
        col = 2
        units = read_sheet.cell_value(r_row, col)
        if units != '':
            mp = bill_row_scrapper(read_sheet, dummy, r_row, col,
                            resco_0b_mos, resco_1b_date, resco_x_NULL,
                            resco_x_NULL, resco_4_payee, resco_x_NULL,
                            resco_6b_resource, resco_7_description, resco_8_unitprice,
                            resco_x_NULL, resco_x_NULL, resco_11b_qty,
                            resco_x, resco_13_subtotal, resco_x_NULL,
                            resco_15_total)

            row_data_list = [cel for cel in mp]
            print(row_data_list)

            my_dict = dict(zip(col_headers, row_data_list))
            df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

        # Now we come to the call blocks. 
        # 
        # first block starts at A103, last block starts at A1192
        # blocks are 33 rows wide, useful data is 22 rows wide

        start_r_row = 104 # tis is the first row of each call block
        info_block = 102 # this is where the data and call info are
        
        # this is the loop over the differnt call blocks
        for call_loop in range(33):
            logger.debug(f"r_row Now = {r_row}")
            r_row = start_r_row + info_block - 102
            # this is the check for running out of calls
            if read_sheet.cell_value(info_block, 0) == 'CALL':
                break
            else:
                # this is a loop over the rows within a call block
                # reg time
                logger.debug(f"Entering callblock Reg")
                for crew_loop in range(18):
                    col = 1
                    units = read_sheet.cell_value(r_row, col)
                    if units != '':
                        call_time_reg = bill_row_scrapper(read_sheet, info_block, r_row, col,
                                                   resco_0_mos, resco_1_date, resco_2_IN,
                                                   resco_3_OUT, resco_4_payee, resco_5_type,
                                                   resco_6_resource, resco_7_description, resco_8_unitprice,
                                                   resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                   resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                   resco_15_total)

                        row_data_list = [cel for cel in call_time_reg]
                        print(row_data_list)

                        my_dict = dict(zip(col_headers, row_data_list))
                        df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

                        r_row += 1

                    else:
                        r_row += 1
                # ot
                logger.debug(f"Entering callblock OT")
                r_row = start_r_row + info_block - 102
                for i in range(18):
                    logger.debug(f"r_row Now = {r_row}")
                    col = 5
                    units = read_sheet.cell_value(r_row, col)
                    if units != '':
                        call_time_ot = bill_row_scrapper(read_sheet, info_block, r_row, col,
                                                   resco_0_mos, resco_1_date, resco_2_IN,
                                                   resco_3_OUT, resco_4_payee, resco_5_type,
                                                   resco_6_resource, resco_7_description, resco_8_unitprice,
                                                   resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                   resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                   resco_15_total)

                        row_data_list = [cel for cel in call_time_ot]
                        print(row_data_list)

                        my_dict = dict(zip(col_headers, row_data_list))
                        df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

                        r_row += 1

                    else:
                        r_row += 1
                    
                # dt
                logger.debug(f"Entering callblock DT")
                r_row = start_r_row + info_block - 102
                for i in range(18):
                    logger.debug(f"r_row Now = {r_row}")
                    col = 9
                    units = read_sheet.cell_value(r_row, col)
                    if units != '':
                        call_time_dt = bill_row_scrapper(read_sheet, info_block, r_row, col,
                                                   resco_0_mos, resco_1_date, resco_2_IN,
                                                   resco_3_OUT, resco_4_payee, resco_5_type,
                                                   resco_6_resource, resco_7_description, resco_8_unitprice,
                                                   resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                   resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                   resco_15_total)

                        row_data_list = [cel for cel in call_time_dt]
                        print(row_data_list)

                        my_dict = dict(zip(col_headers, row_data_list))
                        df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

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

    df_bill_data.to_excel(f'{cfg.desktop_dir}\cpo_bills_records.xlsx', index=False)


if __name__ == '__main__':
    logger.info('~~~The fiile resco_bill_scrape.py has started~~~')
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
    logger.info('~~~~The fiile resco_bill_scrape.py has finished OK~~~')
