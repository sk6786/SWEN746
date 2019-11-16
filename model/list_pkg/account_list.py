from singleton.singleton import Singleton
from pymongo.database import Database
from model.list_pkg.list import List
from model.account_pkg.account import Account


class AccountList(List, Singleton):
    """
    Abstract Class for the Template Method. A List is a Dictionary of an Identification Card to the corresponding object.
    The Dictionary is holds the mapping for all instances of a type of object for the program. Reflects the objects stored
    in MongoDB. All Lists are able to manipulate their Dictionaries appropriately; it is the responsibility of the Concrete
    Classes to make the appropriate changes to the MongoDB.

    NOTE: All subclasses should be final and implement the Singleton design pattern.
    """

    # ----------
    # Attributes
    # ----------
    E = Account
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
        pass

    def mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        pass

    def mongo_update_entry(self, entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param entry: Instance of the entry to update in the database.
        :return: void.
        """
        pass

    def populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        pass
