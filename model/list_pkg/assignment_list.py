from model.list_pkg.list import List
from model.assignment import Assignment


class AssignmentList(List):

    def __init__(self):
        List.__init__(self, Assignment.__class__)

    def mongo_save_entry(self, entry):
        pass

    def mongo_delete_entry(self, entry):
        pass

    def populate_list(self):
        pass
