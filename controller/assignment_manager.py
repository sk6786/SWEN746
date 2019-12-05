from model.assignment import Assignment
from model.list_pkg.assignment_list import AssignmentList
from model.list_pkg.account_list import AccountList
from model.list_pkg.artifact_list import ArtifactList

class AssignmentManager:

    def __init__(self):
        self.assignment_list = AssignmentList()
        self.account_list = AccountList()
        self.artifact_list = ArtifactList()

    def create_assignment(self, paper_id, author_id):
        paper = self.artifact_list.get_entry(paper_id)
        author = self.account_list.get_entry(author_id)
        assignment_id = paper_id
        assignment = Assignment(assignment_id, Assignment.Status.WAITING_FOR_REVIEWS, paper, author)
        self.assignment_list.add_entry(assignment_id,assignment)

    def volunteer_paper(self, account_id, paper_id):
        account_id = self.account_list.get_entry(account_id)
        assignment = self.assignment_list.get_entry(paper_id)
        assignment.pcm_volunteer(account_id)
        self.assignment_list.update_entry(paper_id, assignment)

    def get_volunteerable_papers(self):
        lst = []
        assignments = self.assignment_list.get_list()
        for i in assignments:
            if assignments[i].status == Assignment.Status.WAITING_FOR_REVIEWS:
                lst.append(assignments[i].paper.create_entry_dictionary())
        return lst