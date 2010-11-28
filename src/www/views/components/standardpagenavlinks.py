import cherrypy

from compositecomponent import CompositeComponent
from lib.xmlhelper import XmlHelper
from views.components.xmlcomponent import XmlComponent
from model.account import Account

class StandardPageNavLinks(CompositeComponent):

    def __init__(self):
        super(StandardPageNavLinks, self).__init__(
            tagname='div',
            attributes={'id': 'mainNavLinksContainer'})
        
        self.__create_main_nav_group()
        self.__create_secondary_nav_group()
        
    def __create_main_nav_group(self):
        accountId = cherrypy.session.get('account-id')
        
        navData = [('a', '/login', 'Log In'),
            ('a', '/help', 'Help')]
        
        if accountId:
            sal = Account.get_greeting_name(accountId)
            navData = [
                ('rawstring', self.__userGreetingAreaMarkup.format(sal)),
                ('a', '/help', 'Help')]
            
        navList = self.__create_nav_list(navData)
        XmlHelper.add_class(navList.root, 'mainNavList')
        self.add_component(navList)
        
    def __create_secondary_nav_group(self):
        navData = [
            ('a', '/post', 'Post Item'),
            ('a', '/open-account', 'Open An Account'),
            ('a', '/explore', 'Explore Your Market')
        ]
        
        navList = self.__create_nav_list(navData)
        XmlHelper.add_class(navList.root, 'otherNavList')
        self.add_component(navList)
        
    # left-pointing pointer - &#9668; 
    __userGreetingAreaMarkup = '''
<span id="userGreetingArea"><span>{0}</span><small>&#9660;</small>
    <div id="userMenu" class="popupMenu" style="display: none">
        <a href="/account/settings">Settings</a>
        <a href="/logout">Logout</a>
    </div>
</span>
'''

    def __create_nav_list(self, navData):        
        # create outer nav
        nav = XmlComponent(tagname='nav')
        
        # create ul
        ul = XmlHelper.create_subelement(parent=nav.root, tagname='ul')
        
        # add list item elements
        first = True
        current = None
        for i in navData:
            current = XmlHelper.create_subelement(parent=ul, tagname='li')
            XmlHelper.add_class(current, 'navCell')
            
            if first:
                XmlHelper.add_class(current, 'first')
                first = False
            
            print(i)
            
            if i[0] == 'a':    
                XmlHelper.create_subelement(
                    parent=current,
                    tagname='a',
                    attributes={'href':i[1]},
                    text=i[2])
            elif i[0] == 'span':
                XmlHelper.create_subelement(
                    parent=current,
                    tagname='span',
                    text=i[1])
            elif i[0] == 'rawstring':
                current.append(XmlHelper.from_string(i[1]))
        
        return nav