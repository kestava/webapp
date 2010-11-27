import pprint

import cherrypy

from controllers.homepagecontroller import HomePageController
from controllers.xrdscontroller import XrdsController
from views import create_view
from loginpages import LoginPages

class RootPages(object):

    login = LoginPages()

    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def index(self):
        c = HomePageController()
        return create_view(c)
        
    @cherrypy.expose
    def logout(self):
        if cherrypy.session.has_key('account-id'):
            cherrypy.session.pop('account-id')
            
        raise cherrypy.HTTPRedirect('/')
        
    @cherrypy.expose(alias='xrds.xml')
    def handle_xrds(self):
        c = XrdsController()
        return create_view(c)