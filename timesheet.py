'''

'''

# imported from the standard library
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg

class timesheet:

    def __init__(self, version, name_row, name_column, start_data_row, start_data_col, end_data_row, space_per_day):
        self.version = version
        self.name_row = name_row
        self.name_column = name_column
        self.start_data_row = start_data_row
        self.start_data_col = start_data_col
        self.end_data_row = end_data_row
        self.space_per_day = space_per_day

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

class ts_2015(timesheet):

    #grab the date
    #W PRINT
    def ts15_grabdate(self, wdate_rsheet, wdate_rrow, wdate_rcol, date_wsheet, wdate_wrow, wdate_wcol):
        data = wdate_rsheet.cell_value(wdate_rrow, wdate_rcol)
        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
        day = f"{shift_date_tuple[2]}"
        month = f"{shift_date_tuple[1]}"
        year = f"{shift_date_tuple[0]}"
        shift_date = year + '-' + month + '-' + day
        return shift_date
        #print(shift_date)
        date_wsheet.write(wdate_wrow, wdate_wcol, shift_date)

class ts_casual(timesheet):

    def test(self):
        pass

class ts_2011(timesheet):

    def test2(self):
        pass
