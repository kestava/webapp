from pprint import pprint, pformat
import logging

import cherrypy

class ErrorController(object):

    @cherrypy.expose
    def index(self):
        return 'error (index)'

    @cherrypy.expose
    def default(self, *args, **kwargs):
        cherrypy.log.error(
            'default args: {0}'.format(pformat(args)),
            'ErrorController',
            logging.DEBUG)
        cherrypy.log.error(
            'default kwargs: {0}'.format(pformat(kwargs)),
            'ErrorController',
            logging.DEBUG)
        return 'error (default)'
    
    @cherrypy.expose
    def openid(self):
        return 'error (openid)'