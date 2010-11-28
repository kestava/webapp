import cherrypy

from controllers.postcontroller import PostController
from views import create_view

class PostPages(object):

    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def index(self):
        c = PostController()
        return create_view(c)