from flask import Flask
import urllib.parse
from flask_pymongo import PyMongo
from model.list_pkg.list import List
from model.list_pkg.singleton import Singleton
from model.list_pkg.account_list import AccountList
from model.list_pkg.artifact_list import ArtifactList
from model.assignment import Assignment


class AssignmentList(List, Singleton):
    """
    Collection of all the Assignments for the System. Maps AssignmentID to the corresponding Assignment. Concrete class
    in the Template Method design pattern. Also incorporates the Singleton design pattern to prevent different
    collections of Assignments from existing within the System at the same time.
    """

    # ----------
    # Attributes
    # ----------
    E = Assignment
    # See List Class

    # ------------
    # Constructors
    # ------------
    def __init__(self):
        app = Flask(__name__, template_folder="view")
        app.config["MONGO_URI"] = "mongodb+srv://" + urllib.parse.quote_plus("USER2") + ":" + urllib.parse.quote_plus(
            "1q2w3e4r") + "@cluster0-tk7v1.mongodb.net/SAM2020?retryWrites=true&w=majority"
        mongo = PyMongo(app)
        super().__init__(mongo.db['Assignments'])

    # -------
    # Methods
    # -------
    def mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        self._collection.insert_one(entry.create_assignment_hash())

    def mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        self._collection.delete_one({"assignmentID": entry.get_id()})

    def mongo_update_entry(self, old_entry: E, new_entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param old_entry: Instance of the entry to override in the database.
        :param new_entry: Instance of the entry to enter into the database.
        :return: void.
        """
        self._collection.update_one({"assignmentID": old_entry.get_id()}, {"$set": new_entry.create_assignment_hash()})

    def populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        for entry in self._collection.find():
            assignment = self.create_entry_object(entry)
            self._entries[entry["assignmentID"]] = assignment

    def create_entry_object(self, entry):
        """
        Create and return an instance of an object. Parses the parameters to create an instance of the object. This does
        not add the object to the collection if called directly.
        :param entry: Hash of information to create the object.
        :return: Instance of the appropriate object based on the type of List.
        """
        account_list = AccountList()
        artifact_list = ArtifactList()

        assignment_id = entry["assignmentID"]
        paper_id = entry["paperID"]
        author_id = entry["authorID"]
        pcc_id = entry["pccID"]
        report_id = entry["reportID"]
        reviews = entry["reviews"]
        status_value = entry["status"]
        status = None

        if status_value == Assignment.Status.WAITING_FOR_REVIEWS.value:
            status = Assignment.Status.WAITING_FOR_REVIEWS
        elif status_value == Assignment.Status.WAITING_FOR_REPORT.value:
            status = Assignment.Status.WAITING_FOR_REPORT
        elif status_value == Assignment.Status.COMPLETED.value:
            status = Assignment.Status.COMPLETED

        paper = artifact_list.get_entry(paper_id)
        author = account_list.get_entry(author_id)

        pcc = account_list.get_entry(pcc_id)
        report = artifact_list.get_entry(report_id)

        pcm_reviews = dict()
        for pcm_id in reviews:
            pcm = account_list.get_entry(pcm_id)
            review = artifact_list.get_entry(reviews[pcm_id])
            pcm_reviews[pcm] = review
        reviews = pcm_reviews

        return Assignment(assignment_id, status, paper, author, reviews, report, pcc)

    def get_list_json(self):
        """
        Creates and returns a JSON file representing the Dictionary for the List object. The first JSON object will be
        the lowercase name of the type of entry being stored.
        :return: JSON file representing the collection.
        """
        assignments = []

        for entry_id in self._entries.keys():
            assignments.append(self._entries[entry_id].create_assignment_hash())
        return assignments

    def get_entry_json(self, entry_id: int):
        """
        Create and return a JSON representing the entry at the corresponding id location.
        :param entry_id: int id of the entry.
        :return: JSON format for the entry.
        """
        return self._entries[entry_id].create_assignment_hash()
