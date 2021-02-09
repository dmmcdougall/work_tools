"""
This file is where my general functions are stored
"""


# imported from standard library

# imported from third party repos

# imported from local directories


# TODO: finish docstrings
def add_row_to_df(my_list, my_headers, my_df):
    """ This function takes a list of elements and a list of
    dataframe column headers and adds it to an existing dataframe.

    :param my_list: This is a list of records ready to be added to a dataframe.
    :type my_list: list
    :param my_headers: This is a list of dataframe column headers.
    :type my_headers: list
    :param my_df: This is the dataframe to be appended to.
    :type my_df: object
    :return: A pre-existing dataframe with a single new record set appended to it.
    :rtype: object
    """
    my_dict = dict(zip(my_headers, my_list))
    my_df = my_df.append(my_dict, ignore_index=True)


def convert_date_to_excel_ordinal(day, month, year):
    """ This function takes a date formatted as three integers
    and returns an excel ordinal normal equivalent.

    :param day: The numbered day of the monmth.
    :type day: int
    :param month: the numbered month of the year.
    :type month: integer
    :param year: The year as number.
    :type year: integer
    :return: An excel ordinal number equivalent to teh entered date.
    :rtype: float
    """
    # Python serial numbers start from Jan1 of year 1 whereas excel starts from 1 Jan 1900 so apply an offset
    offset = 693594
    my_date = dt.date(year, month, day)
    n = my_date.toordinal()
    return (n - offset)


"""
This group of functions is a series of generators for taking in functions and runnning them on .xlsx 
sheets so one can return multiple records to form a recorde set in a dataframe
"""

def fnc_spinner_full(sheet, row, my_cls, *args, **kwargs):
    """
    The fnc_spinner series is a generator built to assist in creating a dataframe by taking several functions as inputs
    and returning each one in order so as to create a full record set for each column of the dataframe.
    This generator requires specific variables associated with .xlsx timesheets.
    Example: >>>test = fnc_spinner(read_sheet, r_row, ts_cas,
        grab_01_crew_alpha, grab_02_crew_id,
        grab_01_crew_alpha1=ts_cas.name_row, grab_01_crew_alpha2=ts_cas.name_column,
        grab_02_crew_id1=ts_cas.name_row, grab_02_crew_id2=ts_cas.name_column)
            >>>scraped_data_list = [data for data in test]
            >>>print(scraped_data_list)
            [STA, 4966]
    :param sheet: This argument is the active .xlsx defined by xlrd
    :type: object
    :param row: This argument is the row of data in the .xlsx that we are reading from
    :type: integer
    :param my_cls: This argument is the class instance of the timesheet. This is
        required to select the correct columns of data from teh .xlsx sheet
    :type: object
    :param args: This argument is the function to be run
    :type:object
    :param kwargs: This argument is the keyword arguments. These most be formatted as the name of the function
        followed by a single integer, in order
    :type: string
    :return:The result of each function one record at a time creating a full record set
    :rtype: object
    """
    for i in range(len(args)):
        func = args[i]
        function_name = func.__name__
        key_list = list(kwargs.keys())
        argument_list = [my_str for my_str in key_list if function_name in my_str]
        sorted_keys = sorted(argument_list)
        if not argument_list:
            logger.info(f'the function spinner is going to pass...{function_name}({sheet}, {row})')
            yield func(sheet, row, my_cls)
        else:
            my_val = [kwargs[x] for x in sorted_keys]
            logger.info(f'arguments for this function are {my_val}')
            logger.info(f'the function spinner is going to pass...{function_name}({sheet}, {row}, {my_val})')
            yield func(sheet, row, my_cls, *my_val)


# runs multiple functions with the same number of arguments
# IE: a = simple_fnc_spinner(mult, add, sub, mult1=6, add1=6, sub1=6, mult2=3, add2=3, sub2=3)
def fnc_spinner_simple(*args, **kwargs):
    for i in range(len(args)):
        func = args[i]
        function_name = func.__name__
        first_param = kwargs.get(function_name + "1")
        second_param = kwargs.get(function_name + "2")
        yield func(first_param, second_param)


# this generator goes along a row of data and scrapes the data using the appropriate function
def row_scrapper(read_sheet, info_block, r_row, col, *args):
    for i in range(len(args)):
        func = args[i]
        function_name = func.__name__
        yield func(read_sheet, info_block, r_row, col)


# this function takes in a function, runs it, prints to screen the result, and appends the result to a list.
# it is for reducing the repeats on the scrape.py loop
# args = (the list to append to, the function to run, the positional arguments of input func)
def from_func_2_db_w_print(my_list, function, *args):
    data = function(*args)
    my_list.append(data)
    print(data)


# above but without the print function
def from_func_2_db(my_list, function, *args):
    data = function(*args)
    my_list.append(data)


if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
