import os.path

import cherrypy

from lib.errors import ApplicationError

class ViewBase(object):

    def __init__(self):
        self.__headers = {}
        self.__args = {}
    
    def set_headers(self):
        # Set the Content-Type header
        cherrypy.tools.response_headers.callable([('Content-Type', self._get_header('Content-Type'))])
        
    def _get_header(self, header):
        raise ApplicationError('Child classes must provide an implementation of _get_header')
            
    def build_output(self):
        raise ApplicationError('Child classes must provide an implementation of build_output')
        
    def before_build_output(self):
        pass
        
    def after_build_output(self):
        pass
        