import cherrypy

class RootPages(object):

    @cherrypy.expose
    def index(self):
        return 'Index'