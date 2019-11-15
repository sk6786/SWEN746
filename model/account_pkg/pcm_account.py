from model.account_pkg.account import Account


class PCMAccount(Account):

    def __init__(self, account_id: int, username: str, password: str):
        super(PCMAccount, self).__init__(account_id, username, password)

    def login(self, username: str, password: str):
        pass

    def change_password(self, oldpass: str, newpass: str):
        pass

    def update(self):
        pass

    def notify_account_change(self):
        pass

    def get_account_id(self):
        return self._account_id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password
