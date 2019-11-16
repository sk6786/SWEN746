from abc import ABC, abstractmethod
from pymongo.database import Database
from typing import TypeVar


class List(ABC):
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
    __mongo = None
    __entries = None
    E = TypeVar('E')

    # ------------
    # Constructors
    # ------------
    def __init__(self, mongo: Database, entry_class: E):
        """
        Creates a new List instance. All subclasses should default to this.
        :param mongo: Database MongoDB to pull from.
        :param entry_class: __class__ Class of the __entries being used.
        """
        self.__mongo = mongo
        self.__entry_type = entry_class
        self.__entries = dict()
        self.populate_list()

    # --------------------------
    # Methods for Concrete Class
    # --------------------------
    @abstractmethod
    def mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        pass

    @abstractmethod
    def mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        pass

    @abstractmethod
    def mongo_update_entry(self, entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param entry: Instance of the entry to update in the database.
        :return: void.
        """
        pass

    @abstractmethod
    def populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        pass

    # --------------------------
    # Methods for List Instances
    # --------------------------
    def add_entry(self, entry_id: int, entry: E):
        """
        Adds a new instance to the List if possible. If the instance can be added to the List, it will also be added to
        the Mongo Database.
        :param entry_id: int ID of the entry to add.
        :param entry: Instance of the entry to add to the List.
        :return: void.
        """
        if entry_id in self.__entries:
            return False
        else:
            self.__entries[entry_id] = entry
            self.mongo_save_entry(entry)
            return True

    def remove_entry(self, entry_id: int):
        """
        Removes an instance of an object from the List if possible. If the instance can be removed, it will also be
        removed from the Mongo Database.
        :param entry_id: int ID of the entry to delete.
        :return: void.
        """
        if id not in self.__entries:
            return False
        else:
            self.mongo_delete_entry(self.__entries.pop(entry_id))
            return True

    def update_entry(self, entry_id: int, entry: E):
        """
        Updates an instance of an object from the List if possible. If the instance can be updated, it will also be
        updated in the Mongo Database.
        :param entry_id: int ID of the entry to update.
        :param entry: Instance of the entry to update in the List.
        :return: void.
        """
        if id not in self.__entries:
            return False
        else:
            self.__entries[entry_id] = entry
            self.mongo_update_entry(entry)

    def get_entry(self, entry_id: int):
        """
        Gets the instance of an object to the corresponding ID.
        :param entry_id: int ID of the desired instance.
        :return: Instance of the corresponding entry, NULL if the entry does not exist.
        """
        return self.__entries[entry_id]

    def get_key(self):
        """
        Gets a list of all the keys (IDs for the __entries) of the List instance.
        :return: Collection of all the keys for the Dictionary.
        """
        return self.__entries.keys()
