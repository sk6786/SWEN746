from abc import ABC, abstractmethod
from typing import TypeVar
import random


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
    E = TypeVar('E')
    _entries = None

    # ------------
    # Constructors
    # ------------
    def __init__(self, mongo):
        """
        Creates a new List instance. All subclasses should default to this.
        :param mongo: Collection from MongoDB to interact with.
        """
        if self._entries is None:
            self._collection = mongo
            self._entries = dict()
            self._populate_list()

    # --------------------------
    # Methods for Concrete Class
    # --------------------------
    @abstractmethod
    def _mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        pass

    @abstractmethod
    def _mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        pass

    @abstractmethod
    def _mongo_update_entry(self, old_entry: E, new_entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param old_entry: Instance of the entry to override in the database.
        :param new_entry: Instance of the entry to enter into the database.
        :return: void.
        """
        pass

    @abstractmethod
    def _populate_list(self):
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
        if entry_id in self._entries:
            return False
        else:
            self._entries[entry_id] = entry
            self._mongo_save_entry(entry)
            return True

    def remove_entry(self, entry_id: int):
        """
        Removes an instance of an object from the List if possible. If the instance can be removed, it will also be
        removed from the Mongo Database.
        :param entry_id: int ID of the entry to delete.
        :return: void.
        """
        if entry_id not in self._entries:
            return False
        else:
            self._mongo_delete_entry(self._entries.pop(entry_id))
            return True

    def update_entry(self, entry_id: int, entry: E):
        """
        Updates an instance of an object from the List if possible. If the instance can be updated, it will also be
        updated in the Mongo Database.
        :param entry_id: int ID of the entry to update.
        :param entry: Instance of the entry to update in the List.
        :return: void.
        """
        if entry_id not in self._entries:
            return False
        else:
            self._mongo_update_entry(self._entries[entry_id], entry)
            self._entries[entry_id] = entry

    def get_list(self):
        """
        Gets the dictionary from the List object.
        :return: Dictionary from the List, mapping int ID to a corresponding Object.
        """
        return self._entries

    def get_entry(self, entry_id: int):
        """
        Gets the corresponding entry to the object id.
        :param entry_id: int id of the entry.
        :return: The corresponding entry in the hash, None if the entry does not exist.
        """
        return self._entries.get(entry_id)

    def create_unique_id(self):
        """
        Creates and returns a new id to be used in the list.
        :return: int number that does not exist as a key.
        """
        unique = random.randint(1,1000)
        while unique in self._entries:
            unique = random.randint
        return unique

    def get_list_json(self):
        """
        Creates and returns a JSON file representing the Dictionary for the List object. The first JSON object will be
        the lowercase name of the type of entry being stored.
        :return: JSON file representing the collection.
        """
        all_entries = []

        for entry_id in self._entries.keys():
            all_entries.append(self._entries[entry_id].create_entry_dictionary())

        return all_entries

    def get_entry_json(self, entry_id: int):
        """
        Create and return a JSON representing the entry at the corresponding id location.
        :param entry_id: int id of the entry.
        :return: JSON format for the entry.
        """
        return self._entries[entry_id].create_entry_dictionary()
