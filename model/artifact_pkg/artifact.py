import enum
from model.list_pkg.entry import Entry

import enum


class Artifact(Entry):

    class ArtifactType(enum.Enum):
        PAPER = "Paper"
        REVIEW = "Review"
        REPORT = "Report"

    def __init__(self, artifact_id: int, corresponding_id: int, artifact_type: ArtifactType, author_id: int, artifact_name: str):
        self._artifact_id = artifact_id
        self._corresponding_id = corresponding_id
        self._artifact_type = artifact_type
        self._author_id = author_id
        self._artifact_name = artifact_name

    def create_entry_dictionary(self):
        return {"artifactID": self._artifact_id,
                "correspondingID": self._corresponding_id,
                "type": self._artifact_type.value,
                "authorID": self._author_id,
                "artifactName": self._artifact_name
                }

    def get_entry_id(self):
        return self._artifact_id

    def set_entry_attributes(self, attributes: {}):
        self._artifact_id = attributes.get("artifactID")
        self._corresponding_id = attributes["correspondingID"]
        self._author_id = attributes["authorID"]
        self._artifact_name = attributes["artifactName"]
        type = attributes["type"]

        if type == Artifact.ArtifactType.PAPER.value:
            self._artifact_type = Artifact.ArtifactType.PAPER
        elif type == Artifact.ArtifactType.REVIEW.value:
            self._artifact_type = Artifact.ArtifactType.REVIEW
        elif type == Artifact.ArtifactType.REPORT.value:
            self._artifact_type = Artifact.ArtifactType.REPORT


class Artifact(Entry):

    class ArtifactType(enum.Enum):
        PAPER = "Paper"
        REVIEW = "Review"
        REPORT = "Report"

    def __init__(self, artifact_id: int, corresponding_id: int, artifact_type: ArtifactType, author_id: int, artifact_name: str):
        self._artifact_id = artifact_id
        self._corresponding_id = corresponding_id
        self._artifact_type = artifact_type
        self._author_id = author_id
        self._artifact_name = artifact_name

        # Attributes for Papers Only
        self._title = None
        self._authors = None
        self._version = None
        self._topic = None

    def create_entry_dictionary(self):
        if self._artifact_type == Artifact.ArtifactType.PAPER:
            return {"artifactID": self._artifact_id,
                    "correspondingID": self._corresponding_id,
                    "type": self._artifact_type.value,
                    "authorID": self._author_id,
                    "artifactName": self._artifact_name,
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
                    "artifactName": self._artifact_name
                    }

    def get_entry_id(self):
        return self._artifact_id

    def set_entry_attributes(self, attributes: {}):
        self._artifact_id = attributes.get("artifactID")
        self._corresponding_id = attributes["correspondingID"]
        self._author_id = attributes["authorID"]
        self._artifact_name = attributes["artifactName"]
        type = attributes["type"]

        if type == Artifact.ArtifactType.PAPER.value:
            self._artifact_type = Artifact.ArtifactType.PAPER
            self._title = attributes["title"]
            self._authors = attributes["authors"]
            self._version = attributes["version"]
            self._topic = attributes["topic"]
        elif type == Artifact.ArtifactType.REVIEW.value:
            self._artifact_type = Artifact.ArtifactType.REVIEW
        elif type == Artifact.ArtifactType.REPORT.value:
            self._artifact_type = Artifact.ArtifactType.REPORT
