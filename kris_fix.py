#NOT CURRENTLY USED

#imported from standard library

#imported from third party repos
import xlrd

#imported from local directories

# write time in...
def kris_fix1(head, write_row, read_row, rsheet, wsheet):
    
    if head == 3:
        data = rsheet.cell_value(read_row, 2)
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
        wsheet.write(write_row, 4, time)
    else:
        data = rsheet.cell_value(read_row, 2)
        if data == '':
            shift_in_tuple = (0, 0, 0, 0, 0, 0)
        else:
            shift_in_tuple = xlrd.xldate_as_tuple(data, 1)
        if shift_in_tuple[3] < 10:
            half1_time = "0%s" % (shift_in_tuple[3])
        else:
            half1_time = "%s" % (shift_in_tuple[3])
        if shift_in_tuple[4] == 0:
            half2_time = "%s0" % (shift_in_tuple[4])
        else:
            half2_time = "%s" % (shift_in_tuple[4])
        time = half1_time + ":" + half2_time
        print(time)
        wsheet.write(write_row, 4, time)

# and time out...
def kris_fix2(head, write_row, read_row, rsheet, wsheet):

    if head == 3:
        data = rsheet.cell_value(read_row, 3)
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
        wsheet.write(write_row, 5, time)

    else:
        data = rsheet.cell_value(read_row, 3)
        if data == '':
            shift_out_tuple = (0, 0, 0, 0, 0, 0)
        else:
            shift_out_tuple = xlrd.xldate_as_tuple(data, 1)
        if shift_out_tuple[3] < 10:
            half1_time = "0%s" % (shift_out_tuple[3])
        else:
            half1_time = "%s" % (shift_out_tuple[3])
        if shift_out_tuple[4] == 0:
            half2_time = "%s0" % (shift_out_tuple[4])
        else:
            half2_time = "%s" % (shift_out_tuple[4])
        time = half1_time + ":" + half2_time
        print(time)
        wsheet.write(write_row, 5, time)

if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
