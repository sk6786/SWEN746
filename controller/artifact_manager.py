from model.artifact_pkg.artifact import Artifact
from model.artifact_pkg.paper import Paper
from model.list_pkg.artifact_list import ArtifactList


class ArtifactManager:

    def __init__(self):
        self.atf_list = ArtifactList()

    def create_artifact(self, artifact_type: Artifact.ArtifactType,
                        author_id: int,
                        artifact_name: str):
        atf_id = self.atf_list.create_unique_id()
        atf = Artifact(atf_id, atf_id, artifact_type, author_id, artifact_name)
        self.atf_list.add_entry(atf_id, atf)

    def create_paper(self, author_id: int, artifact_name: str,
                     title: str, authors: str, version: int, topic: str):
        paper_id = self.atf_list.create_unique_id()
        paper = Paper(paper_id, paper_id, Artifact.ArtifactType.PAPER, author_id, artifact_name, title, authors,
                      version, topic)
        self.atf_list.add_entry(paper_id, paper)



    def get_author_paper(self, author_id):
        entries = self.atf_list.get_list()
        ls = []
        for entry in entries:
            entry_dict = entries[entry].create_entry_dictionary()
            ath_id = entry_dict['authorID']
            if ath_id == author_id:
                art_id = entry_dict['artifactID']
                version = entry_dict['version']
                title = entry_dict['title']
                ls.append({'id': author_id, 'title': title, 'version': version, 'paperId': art_id})
        return ls

