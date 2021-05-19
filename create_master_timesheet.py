"""

"""

# imported from standard library
import os
import xlsxwriter
from win32com.client import Dispatch
import datetime as dt
from openpyxl import workbook 
from openpyxl import load_workbook

# imported from third party repos

# imported from local directories
import config as cfg

def remove_password_xlsx(filename):
    xcl = Dispatch('Excel.Application')
    pw_str = '1234'
    wb = xcl.workbooks.open(filename)
    wb.Unprotect(pw_str)
    wb.UnprotectSharing(pw_str)
    xcl.DisplayAlerts = False
    wb.Save()
    xcl.Quit()

def main():
    # create a write book
    my_date = input("""Give me the Date string you would like...\
    """)
    print()

    print(f"Is {my_date} the string you want?\
        ENTER for 'yes' CTRL+C for no")
    print()
    input()

    wk_end = dt.datetime.strptime(my_date, "%B %d, %Y")
    wk_begin = wk_end - dt.timedelta(days=6)

    # print(my_date)
    # print(wk_begin)

    filename = f"House Crew Timesheets - Week Ends {my_date}.xlsx"
    workbook = xlsxwriter.Workbook(cfg.desktop_dir+"\\"+filename)
    write_file = cfg.desktop_dir+"\\"+filename
    workbook.close()

    print('moving on...')
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

    for i in range(7):
        wb = load_workbook(write_file)
        sheets = wb.sheetnames
        Sheet1 = wb[sheets[i]]
        Sheet1 .cell(row = 21, column = 1).value = wk_begin
        wb.save(write_file) 


    # for sht in range(1,7):
    #     try:
    #         wb = xl.Workbooks.Open(Filename=write_file)
    #         ws = wb.Worksheets(sht)
    #         ws.Cells(1,21).Value = wk_begin
    #         print('a single success')
    #     except:
    #         print("nOpE")

    #     finally:
    #         xl.Quit()
        


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