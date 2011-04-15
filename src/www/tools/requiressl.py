
from pprint import pprint, pformat
import urlparse

import cherrypy

from lib import make_netloc

class RequireSsl(cherrypy.Tool):
    
    def __init__(self):
        super(RequireSsl, self).__init__('on_start_resource', self.__check_flag)
        
    def __check_flag(self, path):
        r = cherrypy.request
        n = 'X-Requested-Ssl'
        if not n in r.headers or r.headers[n] != 'Yes':
            parts = ('https', make_netloc(ssl=True), path, '', '', '')
            uri = urlparse.urlunparse(parts)
            cherrypy.log('Not received via HTTPS. Redirecting to {0}'.format(uri))
            raise cherrypy.HTTPRedirect(uri, 303)
            
    
cherrypy.tools.require_ssl = RequireSsl()