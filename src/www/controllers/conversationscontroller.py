
import cherrypy

class ConversationsController(object):

    @cherrypy.expose
    def users(self):
        return 'user conversations'
        
    @cherrypy.expose
    def items(self):
        return 'item conversations'