import cherrypy

from lib.openidhelper import OpenIdHelper

class OpenIdPages(object):
    
    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def process(self, **kwargs):
        OpenIdHelper.handle_auth_response(kwargs)