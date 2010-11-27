import os.path

import cherrypy

from lib.errors import ApplicationError

class ViewBase(object):

    def __init__(self):
        self.__headers = {}
        self.__args = {}
        self.__output = None
        
    @property
    def headers(self):
        return self.__headers
    
    @property
    def output(self):
        return self.__output
        
    @output.setter
    def output(self, value):
        self.__output = value
        
    def set_headers(self):
        # Content-Type
        cherrypy.response.headers['Content-Type'] = self.headers['Content-Type']
        
        # X-XRDS-Location
        if 'X-XRDS-Location' in self.headers:
            cherrypy.response.headers['X-XRDS-Location'] = self.headers['X-XRDS-Location']
            
    def build_output(self):
        raise ApplicationError('Child classes must provide an implementation of build_output')
        
    def before_build_output(self):
        pass
        
    def after_build_output(self):
        pass
        