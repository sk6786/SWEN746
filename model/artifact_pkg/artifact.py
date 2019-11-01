from abc import ABC, abstractmethod
from Subject import Subject

class Artifact(Subject):

    @abstractmethod
    def upload():
        pass

    @abstractmethod
    def download():
        pass

    @abstractmethod
    def delete(atfID):
        pass

    @abstractmethod
    def attach(account):
        pass

    @abstractmethod
    def deattach(account):
        pass

    @abstractmethod
    def notify():
        pass



