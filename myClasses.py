'''

'''

# imported from the standard library
import re

# imported from third party repos

# imported from local directories
import config as cfg

class timesheet:

    def __init__(self, version, name_row, name_column, start_data_row, start_data_col):
        self.version = version
        self.name_row = name_row
        self.name_column = name_column
        self.start_data_row = start_data_row
        self.start_data_col = start_data_col

    # grab the HeadIDAlpha
    def ts_write_HeadIDAlpha(self, HeadID_rsheet):
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

    def write_date2(self):
        data = wdate_rsheet.cell_value(self.start_data_row, self.start_data_col-2)
        shift_date_tuple = xlrd.xldate_as_tuple(data, 1)
        day = f"{shift_date_tuple[2]}"
        month = f"{shift_date_tuple[1]}"
        year = f"{shift_date_tuple[0]}"
        shift_date = year + '-' + month + '-' + day
        # print(shift_date)
        return shift_date











class salariedHead:

    headCount = 0

    # the instance, 'self' in this case, is always teh first argument
    # in it, you define the class variables, then assign thjose variables to the instance variables
    def __init__(self, headAlphaID, headID, lastName, firstName, dir_path, has_left):
        self.headAlphaID = headAlphaID
        self.HeadID = headID
        self.lastName = lastName
        self. firstName = firstName
        self.dir_path = dir_path
        self.has_left = has_left
        salariedHead.headCount += 1 #this increments every time an employee is created

    #repr allows us to print the list with 'salariedHeads(my_var)'
    def __repr__(self):
        return f"salariedHead({self.HeadID}, '{self.lastName}', '{self.firstName}', '{self.dir_path}', {self.has_left})"

    #concat name
    def fullName(self):
        return f"{self.firstName} {self.lastName}"

    def email(self, domain):
        return self.firstName[0].lower() + self.lastName.lower() + domain

#test data
def testheads():
    Wi = salariedHead('z', 99, 'Wonka', 'Willy', 'N/A', False)
    print(Wi)
    print(Wi.fullName())
    print(Wi.email("@chocolatefactory.com"))
    print(salariedHead.headCount)

class searchDict(dict):

    def search_for_match(self, event):
        return (self[key] for key in self if re.match(key, event))



#test salaried head class
if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    testheads()
