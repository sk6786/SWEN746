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

    def get_assignable_papers(self):
        assignments = self.assignment_list.get_list()
        ls = []
        for i in assignments:
            if assignments[i].status == Assignment.Status.WAITING_FOR_REVIEWS:
                dic = {}
                pcm_str = ""
                rvs = assignments[i].reviews
                paper = assignments[i].paper.create_entry_dictionary()
                dic['Paper'] = paper
                if rvs == {}:
                    pcm_str = ""
                else:
                    for pcm in rvs:
                        if rvs[pcm].value == -2:
                            pcmid = pcm.get_entry_id()
                            pcm_str += self.account_list.get_entry(pcmid).create_entry_dictionary()['username'] + ", "
                paper_id = paper['artifactID']
                pcm_str = pcm_str[:-2]
                dic['PCM'] = pcm_str
                dic['List_PCM'] = self.get_pcm_assign_dic(paper_id)
                ls.append(dic)
        return ls

    def get_pcm_assign_dic(self, paper_id):
        pcm_dic = {}
        assignment = self.assignment_list.get_entry(paper_id)
        rvs = assignment.reviews
        for pcm in rvs:
            if rvs[pcm].value == -1:
                pcm_id = pcm.get_entry_id()
                pcm_name = "*" + pcm.get_username()
                pcm_dic[pcm_name] = pcm_id

        entries = self.account_list.get_list()
        for entry in entries:
            entry_dict = entries[entry].create_entry_dictionary()
            role = entry_dict['role']
            if role == 'PCM':
                username = entry_dict['username']
                acc_id = entry_dict['accountID']
                if '*'+username not in pcm_dic and acc_id >= 0:
                    pcm_dic[username] = acc_id
        return pcm_dic

    def assign_list_pcm(self, paper_id, pcm_id_list):
        assignment = self.assignment_list.get_entry(paper_id)
        for pcm_id in pcm_id_list:
            pcm_acc = self.account_list.get_entry(int(pcm_id))
            assignment.pcc_assign_pcm(pcm_acc)
            self.assignment_list.update_entry(paper_id, assignment)

    def get_pcm_assigned_paper(self, pcm_id):
        ls = []
        assignments = self.assignment_list.get_list()
        for i in assignments:
            rvs = assignments[i].reviews
            as_paper_dic = {}
            for pcm in rvs:
                as_pcm_id = pcm.get_entry_id()
                if int(as_pcm_id) == pcm_id and rvs[pcm].value == -2:
                    paper_id = assignments[i].get_entry_id()
                    as_paper_dic['paperID'] = paper_id
                    tmp_paper_dic = self.artifact_list.get_entry(paper_id).create_entry_dictionary()
                    title = tmp_paper_dic['title']
                    as_paper_dic['title'] = title
                    version = tmp_paper_dic['version']
                    as_paper_dic['fileName'] = title + str(version)
            if as_paper_dic != {}:
                ls.append(as_paper_dic)
        return ls

#
# a = AssignmentManager()
# print(a.get_pcm_assigned_paper(2))
# # print(a.get_assignable_papers())
