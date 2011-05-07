
import cherrypy

class RequireMethod(cherrypy.Tool):

    def __init__(self):
        super(RequireMethod, self).__init__('on_start_resource', self.check)
        
    def check(self, method):
        if not method.lower() == cherrypy.request.method.lower():
            raise cherrypy.HTTPError(400)
        
cherrypy.tools.require_method = RequireMethod()