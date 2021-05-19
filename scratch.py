from win32com.client import Dispatch
import xlsxwriter
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

my_file = cfg.desktop_dir+"\\"+"test.xlsx"
my_book = xlsxwriter.Workbook(cfg.desktop_dir+"\\"+"test.xlsx")
print(my_file)

remove_password_xlsx(my_file)
print('done')

