from abc import ABC, abstractmethod
from model.observer_pkg.subject import Subject


class Observer:

    @abstractmethod
    def update(self, subject: Subject):
        # from model.observer_pkg.subject import Subject
        pass
