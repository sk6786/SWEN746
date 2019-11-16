import enum
from model.observer_pkg.subject import Subject


class Assignment(Subject):
    """

    """

    class Status(enum.Enum):
        """Represents the Status for the Assignment."""
        WAITING_FOR_REVIEWS = 1
        WAITING_FOR_REPORT = 2
        COMPLETED = 3

    # ----------
    # Attributes
    # ----------
    assignment_id = None
    paper = None
    reviews = None
    report = None
    status = None

    # ------------
    # Constructors
    # ------------
    def __init__(self, assignment_id, status, paper, reviews=None, report=None):
        self.assignment_id = assignment_id
        self.status = status
        self.paper = paper
        if reviews is None:
            self.reviews = dict()
        else:
            self.reviews = reviews
        self.report = report

    # -------
    # Methods
    # -------
    def pcm_volunteer(self, pcm):
        if self.status == Assignment.Status.COMPLETED:
            return
        elif pcm in self.reviews.key():
            return
        else:
            self.reviews[pcm] = -1
        pass

    def pcm_remove_volunteer(self, pcm):
        pass

    def pcc_assign_pcm(self, pcm):
        pass

    def pcm_submit_review(self, pcm, review):
        pass

    def pcc_submit_report(self, report):
        pass

    def get_status(self):
        return self.status
