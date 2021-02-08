"""
These are generic group of simple classes built to deal with
timesheets.
"""

# imported from the standard library
import re

# imported from third party repos

# imported from local directories

# this meta-class ceates a list the class instances of a class
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls)

# this is for identifying individuals salaried head staff
class SalariedHead:
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, head_alpha_id, head_id, last_name, first_name, dir_path, has_left):
        self._registry.append(self)
        self.head_alpha_id = head_alpha_id
        self.head_id = head_id
        self.last_name = last_name
        self. first_name = first_name
        self.dir_path = dir_path
        self.has_left = has_left

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

#TODO: this is superceded by IterRegistry I think
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
    def testheads():
        wi = SalariedHead('z', 99, 'Wonka', 'Willy', 'N/A', False)
        print(wi)
        print(wi.full_name())
        print(wi.email("@chocolatefactory.com"))
        print(f"There are/is {len(SalariedHead._registry)} salaried head(s)")

    testheads()
