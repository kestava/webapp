
import cherrypy

class LoginController(object):

    @cherrypy.expose
    def index(self):
        return 'login'