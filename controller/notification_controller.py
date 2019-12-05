import enum
from model.list_pkg.account_list import AccountList
from model.account_pkg.account import Account
from model.account_pkg.author_account import AuthorAccount
from model.account_pkg.pcm_account import PCMAccount
from model.account_pkg.pcc_account import PCCAccount
from model.account_pkg.administrator_account import AdministratorAccount


class NotificationController:

    class NotificationID(enum.Enum):
        AUTHOR_ID = -1
        PCM_ID = -2
        PCC_ID = -3
        ADMIN_ID = -4

    def __init__(self):
        self._accounts = AccountList()

    def _get_notification_account(self, account: Account):
        if isinstance(account, AuthorAccount):
             return self._accounts.get_entry(NotificationController.NotificationID.AUTHOR_ID.value)
        elif isinstance(account, PCMAccount):
            return self._accounts.get_entry(NotificationController.NotificationID.PCM_ID.value)
        elif isinstance(account, PCCAccount):
            return self._accounts.get_entry(NotificationController.NotificationID.PCC_ID.value)
        elif isinstance(account, AdministratorAccount):
            return self._accounts.get_entry(NotificationController.NotificationID.ADMIN_ID.value)

    def get_all_notifications(self, account_id: int):
        notifications = []

        account = self._accounts.get_entry(account_id)
        notification_account = self._get_notification_account(account)

        unique_notification = account.get_notificiations()
        general_notifications = notification_account.get_notifications()

        for notif in unique_notification:
            notifications.append(notif)
        for notif in general_notifications:
            notifications.append(notif)

        return notifications

    def get_all_deadlines(self):
        return {
            "Author": self._accounts.get_entry(NotificationController.NotificationID.AUTHOR_ID.value).get_deadline(),
            "PCM": self._accounts.get_entry(NotificationController.NotificationID.PCM_ID.value).get_deadline(),
            "PCC": self._accounts.get_entry(NotificationController.NotificationID.PCC_ID.value).get_deadline(),
            "Admin": self._accounts.get_entry(NotificationController.NotificationID.ADMIN_ID.value).get_deadline()
        }

    def update_all_deadlines(self, deadlines: {}):
        self._accounts.get_entry(NotificationController.NotificationID.AUTHOR_ID.value).set_deadline(deadlines["Author"])
        self._accounts.get_entry(NotificationController.NotificationID.PCM_ID.value).set_deadline(deadlines["PCM"])
        self._accounts.get_entry(NotificationController.NotificationID.PCC_ID.value).set_deadline(deadlines["PCC"])
        self._accounts.get_entry(NotificationController.NotificationID.ADMIN_ID.value).set_deadline(deadlines["Admin"])

    def delete_notification(self, account_id: int, notification: str):
        account = self._accounts.get_entry(account_id)
        account.remove_notification(notification)

    def add_notification(self, account_id: int, notification: str):
        account = self._accounts.get_entry(account_id)
        account.add_notification(notification)
