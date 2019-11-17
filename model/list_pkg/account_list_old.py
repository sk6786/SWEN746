from model.account_pkg.administrator_account import AdministratorAccount
import pymongo
import urllib.parse


class AccountList:

    __instance = None
    __test = None

    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb+srv://" + urllib.parse.quote_plus("USER2") + ":" + urllib.parse.quote_plus("1q2w3e4r") + "@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")
        self.__db = self.__client.get_database("SAM2020")
        self.__test = 1

    def AccountList(self):
        if AccountList.__instance is None:
            AccountList.__instance = AccountList()
        return AccountList.__instance

    # def get_instance(self):
    #     return self.__instance

a = AccountList()
b = AccountList()
a.__test = 2
print(a)
print(b)
assert a is b
