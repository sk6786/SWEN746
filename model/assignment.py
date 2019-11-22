import enum
from model.account_pkg.account import Account
from model.artifact_pkg.artifact import Artifact


class Assignment:
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
    def __init__(self, assignment_id: int, status: Status, paper: Artifact, author: Account, reviews: dict = None,
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
        super(Assignment, self).__init__()

    # -------
    # Methods
    # -------
    def pcm_volunteer(self, pcm: Account):
        if self.reviews[pcm] == Assignment.CurrentEnrollment.ASSIGNED:
            return
        elif self.reviews[pcm] > 0:
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
