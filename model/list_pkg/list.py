from abc import ABC, abstractmethod


class List(ABC):

    entries = None
    entry_class = None

    def __init__(self, entry_class):
        self.entry_class = entry_class
        self.populate_list()

    @abstractmethod
    def save_entry(self, entry):
        pass

    @abstractmethod
    def delete_entry(self, entry):
        pass

    @abstractmethod
    def update_entry(self, id, entry):
        pass

    @abstractmethod
    def populate_list(self):
        pass

    def add_entry(self, id, entry):
        if (id in self.entries):
            return False
        elif (self.entry_class != entry.__class__):
            return False
        else:
            self.entries[id] = entry
            self.save_entry(entry)
            return True

    def remove_entry(self, id):
        if (id not in self.entries):
            return False
        else:
            self.delete_entry(self.entries.pop(id))
            return True

    def update_entry(self, id, entry):
        if (id not in self.entries):
            return False
        elif (self.entry_class != entry.__class__):
            return False
        else:
            self.remove_entry(self, id)
            self.

    def get_entry(self, id):
        return self.entries[id]

    def get_key(self):
        return self.entries.keys()
