import pprint

import cherrypy

import controllers.homepagecontroller
import views.viewcreator

class RootPages(object):

    @cherrypy.expose
    def index(self):
        c = controllers.homepagecontroller.HomePageController()
        return views.viewcreator.ViewCreator.create_view(c)