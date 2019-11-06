from abc import ABC, abstractmethod
from model.observer_pkg.observer import Observer


class Account(Observer, ABC):

    # def __init__(self):
    #     self.accountID = None
    #     self.username = None
    #     self.password = None

    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def change_password(self, oldpass: str, newpass: str):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def notify_account_change(self):
        pass
