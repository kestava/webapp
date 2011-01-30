import cherrypy

from views.createview import create_view
from controllers.timelinecontroller import TimelineController

class TimelinePages(object):

    @cherrypy.expose
    def index(self):
        c = TimelineController()
        return create_view(c)