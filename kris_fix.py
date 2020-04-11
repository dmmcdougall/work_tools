# Kris changed the formatting of his timesheet to make it more flexible and subsueqently
# killed the scrapper.  This is the work around
# this function is for writing the begin and end times of calls

# imported from standard library

# imported from third party repos
import xlrd

# imported from local directories


# write time in...

def kf_format(klw_row, klr_row, klnew_sheet, klread_sheet, klr_col):
    data = klread_sheet.cell_value(klr_row, klr_col)
    kris_str = str(data)
    count_int = len(kris_str)

    if count_int == 1:
        kris_tuple = (0, data, 0, 0)
    elif count_int == 2:
        kris_tuple = (kris_str[0], kris_str[1], 0, 0)
    elif count_int == 3:
        kris_tuple = (0, kris_str[0], kris_str[1], kris_str[2])
    else:
        kris_tuple = (kris_str[0], kris_str[1], kris_str[2], kris_str[3])

    time = str(kris_tuple[0]) + str(kris_tuple[1]) + ":" + str(kris_tuple[2]) + str(kris_tuple[3])
    print(time)
    klnew_sheet.write(klw_row, klr_col + 2, time)

if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
