
import cherrypy

class MarketDataController(object):

    @cherrypy.expose
    def index(self):
        return 'market data'