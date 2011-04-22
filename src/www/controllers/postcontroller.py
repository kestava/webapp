
import cherrypy

class PostController(object):

    @cherrypy.expose
    def material(self):
        return 'material'
        
    @cherrypy.expose
    def transport(self):
        return 'transport'