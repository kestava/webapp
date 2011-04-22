
import cherrypy

class SearchController(object):

    @cherrypy.expose
    def saved(object):
        return 'saved'