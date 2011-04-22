
import cherrypy

class TransactionsController(object):

    @cherrypy.expose
    def index(self):
        return 'transactions'