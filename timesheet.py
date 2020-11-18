"""
This file holds the classes/subclasses for the timesheets
used in the timesheet scrapping package
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

    def ts_blacks_call(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
        if data != '':
            blacks = 1
        else:
            blacks = 0
        return blacks

    # this is a loop, to grab the date of a call
    def ts_grab_date(self, read_sheet, read_row, data_row_offset):
        i = self.start_data_row
        while i < self.end_data_row:
            if (read_row >= i) and (read_row <= i + 6):
                data = read_sheet.cell_value(i+data_row_offset, 0) # TODO: this data offset could be smarter
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

    @staticmethod
    def ts_event_idts_cas_write_show_num(date_str):
        if date_str[4] == '/':
            new_date = str.split(date_str, '/')
        elif date_str[4] == '-':
            new_date = str.split(date_str, '-')
        else:
            new_date = ""
            print("*****************ERROR************************")
            print("Your 'Crew Write Show Number' method is broken")
            print("*****************ERROR************************")
        if int(new_date[1]) >= 9:
            addon = 1
        else:
            addon = 0
        test = new_date[0]

        def split(word):
            return [char for char in word]

        new_list = split(test)
        dig_4 = int(new_list[3]) + addon
        return '0-3108' + new_list[2] + str(dig_4)

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

    def ts_write_time(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
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
    def ts_cas_shift_types_list():
        return cfg.list_crew_shift_types()
    # TODO: what is going on with the crew list function?

    @staticmethod
    def ts_cas_write_show_num(date_str):
        if date_str[4] == '/':
            new_date = str.split(date_str, '/')
        elif date_str[4] == '-':
            new_date = str.split(date_str, '-')
        else:
            new_date = ""
            print("*****************ERROR************************")
            print("Your 'Crew Write Show Number' method is broken")
            print("*****************ERROR************************")
        if int(new_date[1]) >= 9:
            addon = 1
        else:
            addon = 0
        test = new_date[0]

        def split(word):
            return [char for char in word]

        new_list = split(test)
        dig_4 = int(new_list[3]) + addon
        return '0-3108' + new_list[2] + str(dig_4)


class TS2015(TimeSheet):

    # Kris changed the formatting of his timesheet to make it more flexible and subsequently
    # killed the scrapper.  This is the work around
    # this function is for writing the begin and end times of calls
    def ts_15_kf_format(self, read_sheet, read_row, col_modifier):
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier)
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

    def ts_15_write_acct(self, read_sheet, read_row, col_modifier):
        # the .lower() modifier makes the acct_codes not case sensitive
        data = read_sheet.cell_value(read_row, self.start_data_col + col_modifier).lower()
        print(data)
        acct_num = cfg.acct_codes[data]
        return acct_num

    @staticmethod
    def ts_15_event_id(acct_num, date_str):
        if acct_num != '6210-50-504' and acct_num != '6200-50-504':
            if date_str[4] == '/':
                new_date = str.split(date_str, '/')
            elif date_str[4] == '-':
                new_date = str.split(date_str, '-')
            else:
                new_date = ""
                print("*****************ERROR************************")
                print("Your 'Head Write Show Number' method is broken")
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
