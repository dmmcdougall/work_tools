'''

'''

# imported from the standard library
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg

class timesheet:

    def __init__(self, version, name_row, name_column, start_data_row, start_data_col, end_data_row, spaces_per_day):
        self.version = version
        self.name_row = name_row
        self.name_column = name_column
        self.start_data_row = start_data_row
        self.start_data_col = start_data_col
        self.end_data_row = end_data_row
        self.spaces_per_day = spaces_per_day

    def ts_grab_acct(self, read_sheet, read_row, read_col):
        acct_num = read_sheet.cell_value(read_row, read_col)
        return acct_num

    # grab the HeadIDAlpha
    def ts_grabHeadIDAlpha(self, HeadID_rsheet):
        data = 'z'
        # print(data)
        return data

    # grab the HeadIDAlpha
    def ts_grabempNum(self, empNum_rsheet):
        data = empNum_rsheet.cell_value(self.name_row, self.name_column)
        mylist = (str.split(data))
        var = mylist[0]
        head_num = cfg.dict_heads[var]
        # print(head_num)
        return head_num

    # this is a loop, to iterate over the write_date method
    def ts_grabdate(self, read_sheet, read_row):
        i=self.start_data_row
        while i < self.end_data_row:
            if ((read_row >= i) and (read_row <= i + 6)):
                data = read_sheet.cell_value(i+1, 0)
                #print(data)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = f"{shift_date_tuple[2]}"
                month = f"{shift_date_tuple[1]}"
                year = f"{shift_date_tuple[0]}"
                shift_date = year + '-' + month + '-' + day
                i += self.spaces_per_day
                return shift_date
            else:
                i += self.spaces_per_day

    def ts_grabhrs(self, read_sheet, read_row, read_col):
        data = read_sheet.cell_value(read_row, read_col)
        return data

    def ts_write_time(self, read_sheet, read_row,read_col):
        data = read_sheet.cell_value(read_row, read_col)
        if data == '':
            shift_in_tuple = (0, 0, 0, 0, 0, 0)
        else:
            shift_in_tuple = xlrd.xldate_as_tuple(data, 1)
        if shift_in_tuple[3] < 10:
            half1_time = f"{shift_in_tuple[3]}"
        else:
            half1_time = f"{shift_in_tuple[3]}"
        if shift_in_tuple[4] == 0:
            half2_time = f"{shift_in_tuple[4]}0"
        else:
            half2_time = f"{shift_in_tuple[4]}"
        time = half1_time + ":" + half2_time
        return time



class ts_2015(timesheet):

    def test(self):
        pass

class ts_casual(timesheet):

    def test(self):
        pass

class ts_2011(timesheet):

    def test2(self):
        pass
