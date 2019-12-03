import enum


class Artifact():

    class ArtifactType(enum.Enum):
        PAPER = "Paper"
        REVIEW = "Review"
        REPORT = "Report"

    def __init__(self, artifact_id: int, corresponding_id: int, artifact_type: ArtifactType, author_id: int, artifact_name: str):
        self._artifact_id = artifact_id
        self._corresponding_id = corresponding_id
        self._artifact_type = artifact_type
        self._author_id = author_id
        self.artifact_name = artifact_name

        # Attributes for Papers Only
        self._title = None
        self._authors = None
        self._version = None
        self._topic = None

    def create_artifact_hash(self):
        if self._artifact_type == Artifact.ArtifactType.PAPER:
            return {"artifactID": self._artifact_id,
                    "correspondingID": self._corresponding_id,
                    "type": self._artifact_type.value,
                    "authorID": self._author_id,
                    "artifactName": self.artifact_name,
                    "title": self._title,
                    "authors": self._authors,
                    "version": self._version,
                    "topic": self._topic
                    }
        else:
            return {"artifactID": self._artifact_id,
                    "correspondingID": self._corresponding_id,
                    "type": self._artifact_type.value,
                    "authorID": self._author_id,
                    "artifactName": self.artifact_name
                    }

    def get_id(self):
        return self._artifact_id

    def set_paper_attributes(self, title: str, authors: str, version: float, topic: str):
        self._title = title
        self._authors = authors
        self._version = version
        self._topic = topic
