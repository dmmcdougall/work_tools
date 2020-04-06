#imported from standard library
import os

#imported from third party repos
import xlrd
from xlutils.copy import copy

#imported from local directories
import config as cfg

print()
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("         timesheetscrapper_python3.py file launched")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print()

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
            timesheet2015()
        else: print("this is NOT a timesheet")
    print("All done! Time to save to...")
    print(f"{home}\Desktop\scraped_by_python.xls")
    new_book.save(f"{home}\Desktop\scraped_by_python.xls")
    print()

if __name__ == '__main__':
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()