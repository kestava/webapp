
from views.pagebase import PageBase
from views.components.standardpagenavlinks import StandardPageNavLinks
from views.components.standardpagetitlearea import StandardPageTitleArea

class AccountSettingsPage(PageBase):

    def prepare(self):
        self._add_common_header_files()
        self.add_page_component(StandardPageNavLinks())
        self.add_page_component(StandardPageTitleArea(pageTitle='Account Settings'))
        
    def get_title(self):
        return '{0} | Account Settings'.format(super(AccountSettingsPage, self).get_title())