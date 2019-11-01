from abc import ABC, abstractmethod
from model.observer import Observer

class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer):
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


