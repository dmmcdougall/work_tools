"""
These are generic group of simple classes built to work with numerous modules.
"""

# imported from the standard library
import re

# imported from third party repos

# imported from local directories

#
class IterRegistry(type):
    """This meta-class creates a list of the class instances of a class
    """
    def __iter__(cls):
        return iter(cls)

# TODO:class restructuredtext
class SalariedHead:
    """This class is for identifying individual salaried head staff members.

    :param head_alpha_id: The alphabetic portion of the staff members employee number.
    :type head_alpha_id: string
    :param head_id: The numeric portion of the staff members employee number.
    :type head_id: string
    :param last_name: The employees last name.
    :type last_name: string
    :param first_name: The employees first name.
    :type first_name: string
    :param dir_path: The directory where this employee stores their timesheet.
    :type dir_path: string
    :param has_left: Is the employee still working for us.
    :type has_left: boolean
    """
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
    # def __repr__(self):
    #     return f"salariedHead({self.head_id}, " \
    #            f"'{self.last_name}', " \
    #            f"'{self.first_name}', " \
    #            f"'{self.dir_path}', " \
    #            f"{self.has_left})"

    def full_name(self):
        """"This method returns the fullname of a member of the SalariedHeads class.

        :returns: A first name and last name as a single string
        """
        return f"{self.first_name} {self.last_name}"

    def email(self, domain):
        """"This method returns the email of a member of
        the SalariedHeads class. Our organization uses the
        first letter of teh firstname + the last name to build
        email address

        :param domain: Your domain name with an @ sign.  ie @google.com.
        :type domain: string
        :returns: An email address of an employee as a single string
        """
        return self.first_name[0].lower() + self.last_name.lower() + domain

# this is superceded by IterRegistry I think
# class SearchDict(dict):
#
#     def search_for_match(self, event):
#         return (self[key] for key in self if re.match(key, event))


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
