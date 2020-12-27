"""
This file holds the classes/subclasses for bill templates
used in the resco bill scrapper package
"""

# imported from the standard library

# imported from third party repos

# imported from local directories
import config as cfg
from myClasses import IterRegistry

class MyBill:
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, version_name, check,  prep_row, first_infoblock_row, first_data_block_row, mp_row):
        self._registry.append(self)
        self.version_name= version_name
        self.check=check
        self.prep_row = prep_row
        self.first_infoblock_row=first_infoblock_row
        self.first_data_block_row=first_data_block_row
        self.mp_row=mp_row

# test
if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    print(type(MyBill))

    bill1 = MyBill("2019", "", 93, 102,104,60)
    print(type(bill1))

    bill2 = MyBill("test", "fail", 1,2,3,4)

    a = "fail"

    for b in MyBill._registry:
        if b.check == a:
            print(b.version_name)
        else:
            print("Not this one")