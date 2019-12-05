from model.account_pkg.account import Account


class AdministratorAccount(Account):

    def __init__(self, account_id: int, username: str, password: str, notification: []):
        super(AdministratorAccount, self).__init__(account_id, username, password, Account.Role.ADMIN, notification)

    # @property
    # def _account_id(self):
    #     return self._account_id
    #
    # @_account_id.setter
    # def _account_id(self, acc_id):
    #     self._accountID = acc_id



    # TODO: Add Setters

    def login(self, username: str, password: str):
        pass

    def change_password(self, oldpass: str, newpass: str):
        pass

    def update(self):
        pass

    def notify_account_change(self):
        pass

    def create_template(self, template_type: str):
        pass

    def update_template(self, template_id: int, content: str):
        pass

    def delete_template(self, template_id: int):
        pass

    def set_deadline(self, template_id: int):
        pass

    def reassign_pcm(self, paper_id: int, old_pcm_id: int, new_pcm_id: int):
        pass

    def modify_account(self, account_id: int):
        pass

    def delete_account(self, account_id: int):
        pass

    def get_account_id(self):
        return self._account_id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password
