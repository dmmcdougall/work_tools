"""

"""

# imported from standard library
import os
import xlsxwriter
from win32com.client import Dispatch

# imported from third party repos

# imported from local directories
import config as cfg

def main():
    # create a write book
    filename = "House Crew Timesheets - Week Ends 0000000.xlsx"
    workbook = xlsxwriter.Workbook(cfg.desktop_dir+"\\"+filename)
    write_file = cfg.desktop_dir+"\\"+filename
    workbook.close()

    # create a list of the read_books
    read_dir = cfg.my_dir  # CHANGE THIS FOR YOUR NEEDS
    read_list = os.listdir(read_dir)

    xl = Dispatch("Excel.Application")

    for i in range(len(read_list)):
        read_file = (read_dir + '\\' + read_list[i])

        wb1 = xl.Workbooks.Open(Filename=read_file)
        wb2 = xl.Workbooks.Open(Filename=write_file)

        ws1 = wb1.Worksheets(1)
        ws1.Copy(Before=wb2.Worksheets(i+1))

        wb2.Close(SaveChanges=True)
    xl.Quit()

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                      file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()