"""
These are generic group of simple classes built to deal with
timesheets.
"""

# imported from the standard library
import re

# imported from third party repos

# imported from local directories

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls)

class SalariedHead:

    headCount = 0

    # the instance, 'self' in this case, is always teh first argument
    # in it, you define the class variables, then assign thjose variables to the instance variables
    def __init__(self, head_alpha_id, head_id, last_name, first_name, dir_path, has_left):
        self.head_alpha_id = head_alpha_id
        self.head_id = head_id
        self.last_name = last_name
        self. first_name = first_name
        self.dir_path = dir_path
        self.has_left = has_left
        SalariedHead.headCount += 1  # this increments every time an employee is created

    # repr allows us to print the list with 'salariedHeads(my_var)'
    def __repr__(self):
        return f"salariedHead({self.head_id}, " \
               f"'{self.last_name}', " \
               f"'{self.first_name}', " \
               f"'{self.dir_path}', " \
               f"{self.has_left})"

    # concat name
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def email(self, domain):
        return self.first_name[0].lower() + self.last_name.lower() + domain


# test data
def testheads():
    wi = SalariedHead('z', 99, 'Wonka', 'Willy', 'N/A', False)
    print(wi)
    print(wi.full_name())
    print(wi.email("@chocolatefactory.com"))
    print(f"There are/is {SalariedHead.headCount} salaried head(s)")


class SearchDict(dict):

    def search_for_match(self, event):
        return (self[key] for key in self if re.match(key, event))


# test salaried head class
if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    testheads()
