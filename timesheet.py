"""
This file holds the classes/subclasses for the timesheets
used in the timesheet scrapping package
"""

# imported from the standard library
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg
# TODO: finish docstrings

class TimeSheet:

    def __init__(self, version, name_row, name_column, start_data_row, start_data_col, end_data_row, spaces_per_day):
        self.version = version
        self.name_row = name_row
        self.name_column = name_column
        self.start_data_row = start_data_row
        self.start_data_col = start_data_col
        self.end_data_row = end_data_row
        self.spaces_per_day = spaces_per_day

    def ts_blacks_call(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
        if data != '':
            blacks = 1
        else:
            blacks = 0
        return blacks

    @staticmethod
    def ts_event_id(acct_num, date_str):
        if acct_num != '6210-50-504' and acct_num != '6200-50-504':
            if date_str[4] == '/':
                new_date = str.split(date_str, '/')
            elif date_str[4] == '-':
                new_date = str.split(date_str, '-')
            else:
                new_date = ""
                print("*****************ERROR************************")
                print("Your 'Write Show Number' method is broken")
                print("*****************ERROR************************")
            if int(new_date[1]) >= 9:
                addon = 1
            else:
                addon = 0
            test = new_date[0]

            def split1(word):
                return [char for char in word]

            new_list = split1(test)
            dig_4 = int(new_list[3]) + addon
            return '0-3108' + new_list[2] + str(dig_4)
        else:
            data = ''
        return data

    # this is a loop, to grab the date of a call
    def ts_grab_date(self, read_sheet, read_row, data_row_offset):
        i = self.start_data_row
        while i < self.end_data_row:
            if (read_row >= i) and (read_row <= i + 6):
                data = read_sheet.cell_value(i+data_row_offset, 0) # TODO: this data offset could be smarter
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = f"{shift_date_tuple[2]}"
                month = f"{shift_date_tuple[1]}"
                year = f"{shift_date_tuple[0]}"
                shift_date = year + '-' + month + '-' + day
                i += self.spaces_per_day
                return shift_date
            else:
                i += self.spaces_per_day

    def ts_grab_hrs(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
        if data == '':
            data = 0
        return data

    def ts_mp(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
        if data == 1:
            mp = 1
        else:
            mp = 0
        return mp

    def ts_print_my_name(self, read_sheet):
        print()
        print("~~~~"+read_sheet.cell_value(self.name_row, self.name_column)+"~~~~")
        print()

    def ts_write_time(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
        if not data: # this is to catch the 24:00 glitch in the excel sheet
            time = '00:00'
            return time
        elif isinstance(data, float) and data < 1: # this catches the default data
            shift_tuple = xlrd.xldate_as_tuple(data, 1)
            if shift_tuple[3] < 10:
                half1_time = f"{shift_tuple[3]}"
            else:
                half1_time = f"{shift_tuple[3]}"
            if shift_tuple[4] == 0:
                half2_time = f"{shift_tuple[4]}0"
            else:
                half2_time = f"{shift_tuple[4]}"
            time = half1_time + ":" + half2_time
            return time
        elif isinstance(data, float) and data > 1: # this catches a float with no ':', ie '0900'
            my_str = str(data)
            split_str = my_str.split(".")
            kris_str = split_str[0]
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
            return time
        else: # this one is for kris who turned it into an int just to be a dick
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
            return time


class TS2011(TimeSheet):

    def test2(self):
        pass


class TSCasual(TimeSheet):

    @staticmethod
    def ts_cas_write_acct():
        data = '6230-50-504'
        return data

    @staticmethod
    def ts_cas_write_shift_type():
        data = 9
        return data

    @staticmethod
    def ts_cas_shift_types_list(shift_type):
        casual_type = cfg.list_crew_shift_types()
        data = casual_type.get(shift_type)
        return data


class TS2015(TimeSheet):

    def ts_15_write_acct(self, read_sheet, read_row, col_modifier):
        # the .lower() modifier makes the acct_codes not case sensitive
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier).lower()
        acct_num = cfg.acct_codes[data]
        return acct_num

if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()