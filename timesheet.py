"""

"""

# imported from the standard library
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg


class TimeSheet:

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

    # this is a loop, to iterate over the write_date method
    def ts_grab_date(self, read_sheet, read_row):
        i = self.start_data_row
        while i < self.end_data_row:
            if (read_row >= i) and (read_row <= i + 6):
                data = read_sheet.cell_value(i+1, 0)
                # print(data)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = f"{shift_date_tuple[2]}"
                month = f"{shift_date_tuple[1]}"
                year = f"{shift_date_tuple[0]}"
                shift_date = year + '-' + month + '-' + day
                i += self.spaces_per_day
                return shift_date
            else:
                i += self.spaces_per_day

    def ts_grab_hrs(self, read_sheet, read_row, read_col):
        data = read_sheet.cell_value(read_row, read_col)
        if data == '':
            data = 0
        return data

    def ts_write_time(self, read_sheet, read_row, read_col):
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

    def ts_blacks_call(self, read_sheet, read_row, read_col):
        data = read_sheet.cell_value(read_row, read_col)
        if data != '':
            blacks = 1
        else:
            blacks = 0
        return blacks

    def ts_mp(self, read_sheet, read_row, read_col):
        data = read_sheet.cell_value(read_row, read_col)
        if data == 1:
            mp = 1
        else:
            mp = 0
        return mp


class TS2015(TimeSheet):

    # grab the HeadIDAlpha
    def ts_grab_head_id_alpha(self, head_id_read_sheet):
        data = 'z'
        # print(data)
        return data


class TSCasual(TimeSheet):

    def ts_cas_write_acct(self):
        return '6230-50-504'

    def ts_cas_write_shift_type(self):
        data = 1
        return data
        # TODO :check this num

    def ts_cas_write_show_num(self, date_str):
        def split(word):
            return [char for char in word]

        if date_str[4] == '/':
            new_date = str.split(date_str, '/')
        elif date_str[4] == '-':
            new_date = str.split(date_str, '-')
        else:
            new_date = ""
            print("Your 'Crew Write Code' method is broken")
        if int(new_date[1]) >= 9:
            addon = 1
        else:
            addon = 0
        test = new_date[0]
        new_list = split(test)

        dig_4 = int(new_list[3]) + addon

        return '0-3108' + new_list[2] + str(dig_4)


class TS2011(TimeSheet):

    def test2(self):
        pass
