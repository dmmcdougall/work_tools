"""
This file holds the classes/subclasses for bill templates
used in the resco bill scrapper package.  It helps to differentiate the
templates as they are changed over time.
"""

# imported from the standard library

# imported from third party repos

# imported from local directories
from my_classes import IterRegistry


class MyBill:
    """
    This class is for differentiating the billing templates.

    This class includes the metaclass IterRegistry for making the instances iterable.

    :param version_name: This is an intelligent placeholder name of this instance.
    :type version_name: string
    :param check: This is a check performed to now what is in cell A60.
    :type check: string
    :param prep_row: This is the first row of the prep time on the bill.
    :type prep_row: integer
    :param first_infoblock_row: This is the first row of the call block.
    :type first_infoblock_row: integer
    :param first_data_block_row: This is the first call within the call block.
    :type first_data_block_row: integer
    :param mp_row: This is the containging the MP info.
    :type mp_row: integer

    """
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


if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    print(type(MyBill))

    bill1 = MyBill("2019", "", 93, 102,104,60)
    print(type(bill1))

    bill2 = MyBill("test_file_name", "fail", 1,2,3,4)

    a = "fail"

    for b in MyBill._registry:
        if b.check == a:
            print(b.version_name)
        else:
            print("Not this one")