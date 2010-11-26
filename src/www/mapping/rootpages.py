import pprint

import cherrypy

import controllers.homepagecontroller
import views.viewcreator
from loginpages import LoginPages

class RootPages(object):

    login = LoginPages()

    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def index(self):
        c = controllers.homepagecontroller.HomePageController()
        return views.viewcreator.ViewCreator.create_view(c)