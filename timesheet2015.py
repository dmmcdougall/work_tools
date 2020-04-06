#imported from standard library


#imported from third party repos

#imported from local directories
import config as cfg
from myClasses import searchDict


def timesheet2015():

    ts_row = w_row #changing the namespace of w_row so I can adjust it.
    r_row = 19  # r_row is now the read_book row

    # A loop to iterate through the time slots one at a time
    for r_row in range(19, 68):
        # Find the first slot with data
        if read_sheet.cell_type(r_row, 2) != 0:
            print("writing data")

            # write the HeadAlphaID
            data = 'z'
            new_sheet.write(ts_row, 1, data)

            # write persons employee number
            data = read_sheet.cell_value(15, 2)
            my_dict = searchDict(cfg.dict_heads)
            for head_num in my_dict.search_for_match(data):
                new_sheet.write(ts_row, 2, head_num)

                # write date
            if ((r_row >= 19) and (r_row <= 25)):  # SUNDAY
                data = read_sheet.cell_value(20, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)
            elif ((r_row >= 26) and (r_row <= 32)):  # MONDAY
                data = read_sheet.cell_value(27, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)

            elif ((r_row >= 33) and (r_row <= 39)):  # TUESDAY
                data = read_sheet.cell_value(34, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)
            elif ((r_row >= 40) and (r_row <= 46)):  # WEDNESDAY
                data = read_sheet.cell_value(41, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)
            elif ((r_row >= 47) and (r_row <= 53)):  # THURSDAY
                data = read_sheet.cell_value(48, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)
            elif ((r_row >= 54) and (r_row <= 60)):  # FRIDAY
                data = read_sheet.cell_value(55, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)
            elif ((r_row >= 61) and (r_row <= 67)):  # SATURDAY
                data = read_sheet.cell_value(62, 0)
                shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
                day = "%s" % (shift_date_tuple[2])
                month = "%s" % (shift_date_tuple[1])
                year = "%s" % (shift_date_tuple[0])
                shift_date = day + '/' + month + '/' + year
                new_sheet.write(ts_row, 3, shift_date)
                print(shift_date)

            # write time in

            kris_fix1()


                # else:
                #     data = read_sheet.cell_value(r_row, 2)
                #     if data == '':
                #         shift_in_tuple = (0, 0, 0, 0, 0, 0)
                #     else:
                #         shift_in_tuple = xlrd.xldate_as_tuple(data, 1)
                #     if shift_in_tuple[3] < 10:
                #         half1_time = "0%s" % (shift_in_tuple[3])
                #     else:
                #         half1_time = "%s" % (shift_in_tuple[3])
                #     if shift_in_tuple[4] == 0:
                #         half2_time = "%s0" % (shift_in_tuple[4])
                #     else:
                #         half2_time = "%s" % (shift_in_tuple[4])
                #     time = half1_time + ":" + half2_time
                #     print(time)
                #     new_sheet.write(ts_row, 4, time)

                ## ...and time   out

                kris_fix2()

                # else:
                #     data = read_sheet.cell_value(r_row, 3)
                #     if data == '':
                #         shift_out_tuple = (0, 0, 0, 0, 0, 0)
                #     else:
                #         shift_out_tuple = xlrd.xldate_as_tuple(data, 1)
                #     if shift_out_tuple[3] < 10:
                #         half1_time = "0%s" % (shift_out_tuple[3])
                #     else:
                #         half1_time = "%s" % (shift_out_tuple[3])
                #     if shift_out_tuple[4] == 0:
                #         half2_time = "%s0" % (shift_out_tuple[4])
                #     else:
                #         half2_time = "%s" % (shift_out_tuple[4])
                #     time = half1_time + ":" + half2_time
                #     print(time)
                #     new_sheet.write(ts_row, 5, time)


                # write reg time, ot, dt
                w_col = 8
                data = read_sheet.cell_value(r_row, 4)
                new_sheet.write(ts_row, w_col, data)
                w_col = w_col + 1

                data = read_sheet.cell_value(r_row, 5)
                new_sheet.write(ts_row, w_col, data)
                w_col = w_col + 1

                data = read_sheet.cell_value(r_row, 6)
                new_sheet.write(ts_row, w_col, data)

                # write accounting code
                data = read_sheet.cell_value(r_row, 8)
                print(data)
                my_dict = searchDict(cfg.acct_codes)
                for acct_num in my_dict.search_for_match(data):
                    new_sheet.write(ts_row, 11, acct_num)

                # write show data
                data = 'J'  # this is year specific CHANGE THIS FOR YOUR NEEDS
                new_sheet.write(ts_row, 6, data)

                data = '0-310820'  # this is year specific
                if acct_num != '6210-50-504' and acct_num != '6200-50-504':
                    new_sheet.write(ts_row, 7, data)
                # elif acct_num != '6200-50-504':
                #   new_sheet.write(ts_row, 7, data)
                else:
                    new_sheet.write(ts_row, 7, "")

                # showcall true/false
                data = read_sheet.cell_value(r_row, 9)
                if data != '':
                    new_sheet.write(ts_row, 12, 1)
                else:
                    new_sheet.write(ts_row, 12, 0)

                # Meal Penalty true/false
                data = read_sheet.cell_value(r_row, 7)
                if data == 1:
                    new_sheet.write(ts_row, 13, 1)
                else:
                    new_sheet.write(ts_row, 13, 0)

                ts_row = ts_row + 1  # move along in the write_book

            else:
                print("no data in cel E" + str((r_row) + 1))  # move on to the next time slot

if __name == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
