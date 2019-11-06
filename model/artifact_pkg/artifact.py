from abc import ABC, abstractmethod
from model.observer_pkg.subject import Subject
from model.observer_pkg.observer import Observer


class Artifact(Subject):

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def delete(self, atf_id):
        pass

    @abstractmethod
    def attach(self, account:Observer):
        pass

    @abstractmethod
    def deattach(self, account: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass



