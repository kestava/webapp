
from controllerbase import ControllerBase
from views.account.accountsettingspage import AccountSettingsPage

class AccountSettingsController(ControllerBase):

    def create_view(self):
        v = AccountSettingsPage()
        v.prepare()
        return v