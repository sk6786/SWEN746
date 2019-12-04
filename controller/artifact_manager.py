from model.artifact_pkg.artifact import Artifact
from model.list_pkg.artifact_list import ArtifactList


class ArtifactManager:

    def __init__(self):
        self.atf_list = ArtifactList()

    def create_artifact(self, artifact_type: Artifact.ArtifactType,
                        author_id: int,
                        artifact_name: str):
        entry = self.atf_list.create_entry_object({'type': artifact_type, 'authorID': author_id,
                                                   'artifactName': artifact_name})
        self.atf_list.add_entry(entry.artifact_id, entry)

    def create_paper(self, author_id: int, artifact_name: str,
                     title: str, authors: str, version: int, topic: str):
        entry = self.atf_list.create_entry_object({'type': 'Paper', 'authorID': author_id, 'artifactName': artifact_name,
                                           'title': title, 'authors': authors, 'version': version, 'topic': topic})
        self.atf_list.add_entry(entry.artifact_id, entry)