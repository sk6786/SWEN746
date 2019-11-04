from abc import ABC, abstractmethod
from model.observer import Subject
class Observer:
    
    @abstractmethod
    def update(self, subject: Subject):
        pass