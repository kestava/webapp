from pprint import pprint, pformat

import cherrypy

class ErrorController(object):

    @cherrypy.expose
    def index(self):
        return 'error (index)'

    @cherrypy.expose
    def default(self, *args, **kwargs):
        print('ErrorController.default args: {0}'.format(pformat(args)))
        print('ErrorController.default kwargs: {0}'.format(pformat(kwargs)))
        return 'error (default)'
    
    @cherrypy.expose
    def openid(self):
        return 'error (openid)'