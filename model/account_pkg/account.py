import enum
from abc import ABC, abstractmethod
from model.observer_pkg.observer import Observer
import pymongo
from pymongo import MongoClient
import urllib.parse


class Account(ABC):

    class Role(enum.Enum):
        AUTHOR = "Author"
        PCM = "PCM"
        PCC = "PCC"
        ADMIN = "Admin"

    def __init__(self, account_id: int, username: str, password: str, role: Role):
        self.account_id = account_id
        self.username = username
        self.password = password
        self.role = role
        self.__client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")

    def get_id(self):
        return self.account_id

    @abstractmethod
    def change_password(self, oldpass: str, newpass: str):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def notify_account_change(self):
        pass
