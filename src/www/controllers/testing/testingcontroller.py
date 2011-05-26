
import cherrypy

class TestingController(object):
    
    def __init__(self):
        
        def _jkl(arg1):
            return arg1
        
        self.abc = lambda:None
        setattr(self.abc, '_def', lambda:None)
        setattr(self.abc._def, 'ghi', lambda:None)
        setattr(self.abc._def.ghi, 'jkl', _jkl)
        
        self.abc._def.ghi.jkl.exposed = True
    
    @cherrypy.expose(alias='createaccount')
    def create_account(self, *args, **kwargs):
        return 'create account'