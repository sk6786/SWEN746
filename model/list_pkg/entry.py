from abc import ABC, abstractmethod


class Entry(ABC):

    @abstractmethod
    def set_entry_attributes(self, attributes: {}):
        pass

    @abstractmethod
    def get_entry_id(self):
        pass

    @abstractmethod
    def create_entry_dictionary(self):
        pass
