from model.list_pkg.list import List
from model.list_pkg.singleton import Singleton
from model.artifact import Artifact


class ArtifactList(List, Singleton):
    """
    Collection of all the Artifacts for the System. Maps ArtifactID to the corresponding Artifact. Concrete class in the
    Template Method design pattern. Also incorporates the Singleton design pattern to prevent different collections of
    Artifacts from existing within the System at the same time.
    """

    # ----------
    # Attributes
    # ----------
    E = Artifact
    # See List Class

    # ------------
    # Constructors
    # ------------
    # See List Class

    # -------
    # Methods
    # -------
    def mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        self._collection.insert_one(entry.create_artifact_hash())

    def mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        self._collection.delete_one({"artifactID": entry.get_id()})

    def mongo_update_entry(self, old_entry: E, new_entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param old_entry: Instance of the entry to override in the database.
        :param new_entry: Instance of the entry to enter into the database.
        :return: void.
        """
        updated_entry = new_entry.create_artifact_hash()
        self._collection.update_one({"artifactID": old_entry.get_id()}, {"$set": updated_entry})

    def populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        for entry in self._collection.find():
            artifact = self.create_entry_object(entry)
            self._entries[entry["artifactID"]] = artifact

    def create_entry_object(self, entry):
        """
        Create and return an instance of an object. Parses the parameters to create an instance of the object. This does
        not add the object to the collection if called directly.
        :param entry: Hash of information to create the object.
        :return: Instance of the appropriate object based on the type of List.
        """
        artifact = None
        artifact_id = entry.get("artifactID", self.create_unique_id())
        corresponding_id = entry["correspondingID"]
        artifact_type = entry["type"]
        author_id = entry["authorID"]
        artifact_name = entry["artifactName"]
        if artifact_type == Artifact.ArtifactType.PAPER.value:
            artifact = Artifact(artifact_id, corresponding_id, Artifact.ArtifactType.PAPER, author_id, artifact_name)
        elif artifact_type == Artifact.ArtifactType.REVIEW.value:
            artifact = Artifact(artifact_id, corresponding_id, Artifact.ArtifactType.REVIEW, author_id, artifact_name)
        elif artifact_type == Artifact.ArtifactType.REPORT.value:
            artifact = Artifact(artifact_id, corresponding_id, Artifact.ArtifactType.REPORT, author_id, artifact_name)
        return artifact

    def get_list_json(self):
        """
        Creates and returns a JSON file representing the Dictionary for the List object. The first JSON object will be
        the lowercase name of the type of entry being stored.
        :return: JSON file representing the collection.
        """
        artifacts = []

        for entry_id in self._entries.keys():
            entry = self._entries[entry_id]
            artifacts.append(entry.create_artifact_hash())

        return artifacts

    def get_entry_json(self, entry_id: int):
        """
        Create and return a JSON representing the entry at the corresponding id location.
        :param entry_id: int id of the entry.
        :return: JSON format for the entry.
        """
        return self._entries[entry_id].create_artifact_hash()
