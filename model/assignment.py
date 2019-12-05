import enum
from model.list_pkg.entry import Entry
from model.account_pkg.account import Account
from model.artifact_pkg.artifact import Artifact
from model.list_pkg.account_list import AccountList
from model.list_pkg.artifact_list import ArtifactList
from model.artifact_pkg.paper import Paper

class Assignment(Entry):
    """

    """

    class Status(enum.Enum):
        """Represents the Status for the Assignment."""
        WAITING_FOR_REVIEWS = 1
        WAITING_FOR_REPORT = 2
        COMPLETED = 3

    class CurrentEnrollment(enum.Enum):
        """Represents how the PCM is connected to the Assignment. A value greater than zero dictates that the PCM has
        completed their task and should not be removed."""
        VOLUNTEERED = -1
        ASSIGNED = -2

    # ------------
    # Constructors
    # ------------
    def __init__(self, assignment_id: int, status: Status, paper: Paper, author: Account, reviews: dict = None,
                 report: Artifact = None, pcc: Account = None):
        self.assignment_id = assignment_id
        self.status = status
        self.paper = paper
        if reviews is None:
            self.reviews = dict()
        else:
            self.reviews = reviews
        self.author = author
        self.pcc = pcc
        self.report = report

    # -------
    # Methods
    # -------
    def create_entry_dictionary(self):

        rev = {}

        for pcm in self.reviews:
            possible_review = self.reviews[pcm]
            if isinstance(possible_review, Artifact):
                rev[str(pcm.get_entry_id())] = self.reviews[pcm].get_entry_id()
            else:
                rev[str(pcm.get_entry_id())] = self.reviews[pcm].value

        if self.pcc is None:
            pcc = None
        else:
            pcc = self.pcc.get_entry_id()

        if self.report is None:
            report = None
        else:
            report = self.report.get_entry_id()

        return {"assignmentID": self.assignment_id,
                "status": self.status.value,
                "paperID": self.paper.get_entry_id(),
                "reviews": rev,
                "authorID": self.author.get_entry_id(),
                "pccID": pcc,
                "reportID": report
                }

    def get_entry_id(self):
        return self.assignment_id

    def set_entry_attributes(self, attributes: {}):
        account_list = AccountList()
        artifact_list = ArtifactList()

        self.assignment_id = attributes["assignmentID"]
        paper_id = attributes["paperID"]
        author_id = attributes["authorID"]
        pcc_id = attributes["pccID"]
        report_id = attributes["reportID"]
        reviews = attributes["reviews"]
        status_value = attributes["status"]

        if status_value == Assignment.Status.WAITING_FOR_REVIEWS.value:
            self.status = Assignment.Status.WAITING_FOR_REVIEWS
        elif status_value == Assignment.Status.WAITING_FOR_REPORT.value:
            self.status = Assignment.Status.WAITING_FOR_REPORT
        elif status_value == Assignment.Status.COMPLETED.value:
            self.status = Assignment.Status.COMPLETED

        self.paper = artifact_list.get_entry(paper_id)
        self.author = account_list.get_entry(author_id)

        self.pcc = account_list.get_entry(pcc_id)
        self.report = artifact_list.get_entry(report_id)

        pcm_reviews = dict()
        for pcm_id in reviews:
            pcm = account_list.get_entry(int(pcm_id))
            pcm_dict_num = reviews[pcm_id]

            if pcm_dict_num < 0:
                if pcm_dict_num == Assignment.CurrentEnrollment.VOLUNTEERED:
                    pcm_reviews[pcm] = Assignment.CurrentEnrollment.VOLUNTEERED
                elif pcm_dict_num == Assignment.CurrentEnrollment.ASSIGNED:
                    pcm_reviews[pcm] = Assignment.CurrentEnrollment.ASSIGNED
            else:
                pcm_reviews[pcm] = artifact_list.get_entry(reviews[pcm_dict_num])
        self.reviews = pcm_reviews

    def pcm_volunteer(self, pcm: Account):
        if pcm in self.reviews:
            return
        else:
            self.reviews[pcm] = Assignment.CurrentEnrollment.VOLUNTEERED

    def pcm_remove_volunteer(self, pcm: Account):
        if self.reviews[pcm] == Assignment.CurrentEnrollment.VOLUNTEERED:
            del self.reviews[pcm]

    def pcc_assign_pcm(self, pcm: Account):
        if self.reviews[pcm] <= 0 and self.reviews[pcm] is not None:
            self.reviews = Assignment.CurrentEnrollment.ASSIGNED

    def pcc_remove_pcm(self, pcm: Account):
        pass

    def pcm_submit_review(self, pcm: Account, review: Artifact):
        if self.reviews[pcm] == Assignment.CurrentEnrollment.ASSIGNED:
            self.reviews[pcm] = review

    def pcc_request_another_review(self, pcm: Account):
        if self.reviews[pcm] > 0:
            self.reviews[pcm] = Assignment.CurrentEnrollment.ASSIGNED

    def pcc_submit_report(self, report: Artifact):
        pass

    def get_status(self):
        return self.status
