import enum
from model.list_pkg.account_list import AccountList
from model.account_pkg.account import Account
from model.account_pkg.author_account import AuthorAccount
from model.account_pkg.pcm_account import PCMAccount
from model.account_pkg.pcc_account import PCCAccount
from model.account_pkg.administrator_account import AdministratorAccount


class NotificationManager:

    class NotificationID(enum.Enum):
        AUTHOR_ID = -1
        PCM_ID = -2
        PCC_ID = -3
        ADMIN_ID = -4

    def __init__(self):
        self._accounts = AccountList()

    def _get_notification_account(self, account: Account):
        if isinstance(account, AuthorAccount):
             return self._accounts.get_entry(NotificationManager.NotificationID.AUTHOR_ID.value)
        elif isinstance(account, PCMAccount):
            return self._accounts.get_entry(NotificationManager.NotificationID.PCM_ID.value)
        elif isinstance(account, PCCAccount):
            return self._accounts.get_entry(NotificationManager.NotificationID.PCC_ID.value)
        elif isinstance(account, AdministratorAccount):
            return self._accounts.get_entry(NotificationManager.NotificationID.ADMIN_ID.value)

    def get_all_notifications(self, account_id: int):
        notifications = []

        account = self._accounts.get_entry(account_id)
        notification_account = self._get_notification_account(account)

        unique_notification = account.get_notifications()
        general_notifications = notification_account.get_notifications()
        notifications.append(self._get_deadline_account(notification_account))
        for notif in unique_notification:
            notifications.append(notif)
        for notif in general_notifications:
            notifications.append(notif)

        return notifications

    def _get_deadline_account(self, account):
        notif = ""
        if account.account_id == NotificationManager.NotificationID.AUTHOR_ID.value:
            notif += "Paper Submission Deadline: "
        elif account.account_id == NotificationManager.NotificationID.PCM_ID.value:
            notif += "Review Submission Deadline: "
        elif account.account_id == NotificationManager.NotificationID.PCC_ID.value:
            notif += "Report Submission Deadline: "
        else:
            notif += ""
        notif += str(account.get_deadline())
        return notif


    def get_all_deadlines(self):
        return {
            "Author": self._accounts.get_entry(NotificationManager.NotificationID.AUTHOR_ID.value).get_deadline(),
            "PCM": self._accounts.get_entry(NotificationManager.NotificationID.PCM_ID.value).get_deadline(),
            "PCC": self._accounts.get_entry(NotificationManager.NotificationID.PCC_ID.value).get_deadline(),
            "Admin": self._accounts.get_entry(NotificationManager.NotificationID.ADMIN_ID.value).get_deadline()
        }

    def update_all_deadlines(self, deadlines: {}):
        if "Author" in deadlines:
            new_author_dead = self._accounts.get_entry(NotificationManager.NotificationID.AUTHOR_ID.value)
            new_author_dead.set_deadline(deadlines["Author"])
            self._accounts.update_entry(NotificationManager.NotificationID.AUTHOR_ID.value, new_author_dead)
        if "PCM" in deadlines:
            new_pcm_dead = self._accounts.get_entry(NotificationManager.NotificationID.PCM_ID.value)
            new_pcm_dead.set_deadline(deadlines["PCM"])
            self._accounts.update_entry(NotificationManager.NotificationID.PCM_ID.value, new_pcm_dead)
        if "PCC" in deadlines:
            new_pcc_dead = self._accounts.get_entry(NotificationManager.NotificationID.PCC_ID.value)
            new_pcc_dead.set_deadline(deadlines["PCC"])
            self._accounts.update_entry(NotificationManager.NotificationID.PCC_ID.value, new_pcc_dead)
        if "Admin" in deadlines:
            new_admin_dead = self._accounts.get_entry(NotificationManager.NotificationID.ADMIN_ID.value)
            new_admin_dead.set_deadline(deadlines["Admin"])
            self._accounts.update_entry(NotificationManager.NotificationID.ADMIN_ID.value, new_admin_dead)

    def delete_notification(self, account_id: int, notification: str):
        account = self._accounts.get_entry(account_id)
        account.remove_notification(notification)
        self._accounts.update_entry(account_id, account)

    def add_notification(self, account_id: int, notification: str):
        account = self._accounts.get_entry(account_id)
        account.add_notification(notification)
        self._accounts.update_entry(account_id, account)
