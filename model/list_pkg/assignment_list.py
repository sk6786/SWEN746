from model.list_pkg.list import List
from model.Assignment import Assignment


class AssignmentList(List):

    def __init__(self):
        List.__init__(self, Assignment.__class__)

    def save_entry(self, entry):
        pass

    def delete_entry(self, entry):
        pass

    def populate_list(self):
        pass
