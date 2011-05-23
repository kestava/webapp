
import cherrypy

from lib.openidhelper import OpenIdHelper

class OpenIDController(object):

    @cherrypy.expose
    def process(self, **kwargs):
        OpenIdHelper.handle_auth_response(kwargs)
        