import cherrypy

from lib.errors import NotImplementedError
from lib.config import Config
from views.pagebase import PageBase

from views.components.standardpagenavlinks import StandardPageNavLinks
from centralcontent import CentralContent
import views.components.compositecomponent
from model.account import Account

class HomepagePage(PageBase):
        
    def prepare(self):
        self._add_common_header_files()
        
        self.add_stylesheet('homepage.css')
        
        if Config.get_environment() == 'development':
            self.add_head_script('homepage.js')
        else:
            self.add_head_script('homepage.min.js')
            
        self.add_page_component(StandardPageNavLinks())
        self.add_page_component(CentralContent())
        