import enum


class Artifact:

    class ArtifactType(enum.Enum):
        PAPER = "Paper"
        REVIEW = "Review"
        REPORT = "Report"

    def __init__(self, artifact_id: int, corresponding_id: int, artifact_type: ArtifactType, author_id: int, artifact_name: str):
        self.artifact_id = artifact_id
        self._corresponding_id = corresponding_id
        self._artifact_type = artifact_type
        self._author_id = author_id
        self.artifact_name = artifact_name

    def create_artifact_hash(self):
        return {"artifactID": self.artifact_id,
                "correspondingID": self._corresponding_id,
                "type": self._artifact_type.value,
                "authorID": self._author_id,
                "artifactName": self.artifact_name
                }

    def get_id(self):
        return self.artifact_id
