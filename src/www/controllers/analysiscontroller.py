
import cherrypy

class AnalysisController(object):

    @cherrypy.expose
    def index(self):
        return 'analysis'