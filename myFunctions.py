"""
This file is where my general functions are stored
"""

# imported from standard library

# imported from third party repos

# imported from local directories
import config as cfg

# this function takes in a function, runs it, prints to screen the result, and appends the result to a list.
# it is for reducing the repeats on the scrape.py loop
# args = (the list to append to, the function to run, the positional arguments of input func)
def from_func_2_db(my_list, function, *args):
    data = function(*args)
    print(data)
    my_list.append(data)
