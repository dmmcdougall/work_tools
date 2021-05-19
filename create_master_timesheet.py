"""

"""

# imported from standard library
import os
import xlsxwriter
from win32com.client import Dispatch
import datetime as dt
import openpyxl
from shutil import copyfile

# imported from third party repos

# imported from local directories
import config as cfg

# def remove_password_xlsx(filename):
#     xcl = Dispatch('Excel.Application')
#     pw_str = '1234'
#     wb = xcl.workbooks.open(filename)
#     wb.Unprotect(pw_str)
#     wb.UnprotectSharing(pw_str)
#     xcl.DisplayAlerts = False
#     wb.Save()
#     xcl.Quit()

def main():
    # get the wk ending info from teh usr
    my_date = input("""Give me the Date string you would like.  An example of the excepted fomrat is...\n
    Sep 14, 1985
    """)
    my_date_comma = my_date.replace(',', '')
    print()
    print(f"Is {my_date} the string you want?")
    print("ENTER for 'yes' CTRL+C for no")
    print()
    input()

    # create dir and copy th files
    dir_name = f"{cfg.desktop_dir}\\Week Ends {my_date}"
    os.mkdir(dir_name)

    # create a list of the read_books
    read_dir = cfg.my_dir  
    read_list = os.listdir(read_dir)
    print(read_list)
    for my_file in read_list:
        file_path = read_dir + '\\' + my_file
        save_path = dir_name + '\\' + my_file
        copyfile(file_path, save_path)

    # create a write book
    wk_end = dt.datetime.strptime(my_date, "%b %d, %Y")
    wk_begin = wk_end - dt.timedelta(days=6)

    filename = f"House Crew Timesheets - Week Ends {my_date_comma}.xlsx"
    workbook = xlsxwriter.Workbook(dir_name+"\\"+filename)
    write_file = dir_name +"\\"+filename
    workbook.close()

    print('moving on...')
    

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
        wb = openpyxl.load_workbook(write_file)
        sheets = wb.sheetnames
        Sheet1 = wb[sheets[i]]
        Sheet1 .cell(row = 21, column = 1).value = wk_begin
        wb.save(write_file) 

    wb = openpyxl.load_workbook(write_file)
    sheet_list = wb.sheetnames
    print(sheet_list)
    wb.remove(wb['Sheet1'])
    wb.save(write_file) 


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