import cherrypy

from views.createview import create_view
from controllers.timelinecontroller import TimelineController

class TimelinePages(object):

    @cherrypy.tools.request_debugging()
    @cherrypy.expose
    def index(self):
        c = TimelineController()
        return create_view(c)