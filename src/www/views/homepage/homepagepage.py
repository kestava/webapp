import cherrypy

from lib.errors import NotImplementedError
from lib.config import Config
from views.pagebase import PageBase

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
            
        # create nav groups
        topDiv = views.components.compositecomponent.CompositeComponent(
            tagname='div',
            attributes={'id': 'mainNavLinksContainer'})
        self._create_main_nav_group(parent=topDiv)
        self._create_secondary_nav_group(parent=topDiv)
        self.add_page_component(topDiv)
        
        self.add_page_component(CentralContent())
        
    def _create_main_nav_group(self, parent):
        accountId = cherrypy.session.get('account-id')
        
        navData = [('a', '/login', 'Log In'),
            ('a', '/help', 'Help')]
        
        if accountId:
            sal = Account.get_greeting_name(accountId)
            navData = [
                ('rawstring', self.__userGreetingAreaMarkup.format(sal)),
                ('a', '/help', 'Help')]
            
        navList = self.create_nav_list(navData)
        navList.add_class('mainNavList')
        parent.add_component(navList)
        
    def _create_secondary_nav_group(self, parent):
        navData = [
            ('a', '/post', 'Post Item'),
            ('a', '/open-account', 'Open An Account'),
            ('a', '/explore', 'Explore Your Market')
        ]
        
        navList = self.create_nav_list(navData)
        navList.add_class('otherNavList')
        parent.add_component(navList)
        
#    __userGreetingAreaMarkup = '''
#<span id="userGreetingArea">{0}<small>&#9660;</small></span>
#'''
        
    __userGreetingAreaMarkup = '''
<span id="userGreetingArea">{0}<small>&#9660;</small>
    <div id="userMenu" class="popupMenu" style="display: none">
        <a href="/account-settings">Settings</a>
        <a href="/logout">Logout</a>
    </div>
</span>
'''
        