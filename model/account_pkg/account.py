from abc import ABC, abstractmethod
from model.observer import Observer

class Account(Observer):

    @abstractmethod
    def login(self):
        pass

