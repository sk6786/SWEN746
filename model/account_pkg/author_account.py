from model.account_pkg.account import Account


class AuthorAccount(Account):

    def __init__(self, account_id: int, username: str, password: str):
        self.__account_id = account_id
        self.__username = username
        self.__password = password

    @property
    def __account_id(self):
        return self.__account_id

    @__account_id.setter
    def __account_id(self, acc_id):
        self.__accountID = acc_id

    # TODO: add other getter and setter

    def login(self, username: str, password: str):
        pass

    def change_password(self, oldpass: str, newpass: str):
        pass

    def update(self):
        pass

    def notify_account_change(self):
        pass

