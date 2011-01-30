import cherrypy

class TimelinePages(object):

    @cherrypy.expose
    def index(self):
        return 'Hey!'