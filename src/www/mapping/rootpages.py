import pprint

import cherrypy

import controllers.homepagecontroller
from views import create_view
from loginpages import LoginPages

class RootPages(object):

    login = LoginPages()

    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def index(self):
        c = controllers.homepagecontroller.HomePageController()
        return create_view(c)
        
    @cherrypy.expose
    def logout(self):
        if cherrypy.session.has_key('account-id'):
            cherrypy.session.pop('account-id')
            
        c = controllers.homepagecontroller.HomePageController()
        return create_view(c)