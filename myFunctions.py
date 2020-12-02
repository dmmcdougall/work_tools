"""
This file is where my general functions are stored
"""

# imported from standard library

# imported from third party repos

# imported from local directories


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

