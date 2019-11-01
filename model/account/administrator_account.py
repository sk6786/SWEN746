
import sys
sys.path.append("D:\Github\SWEN746")
from model.account.Account import Account

class AdministratorAccount(Account):

    def login(self):
        print("login")


a = AdministratorAccount()
a.login()

