
import cherrypy

from lib.sessionhelper import SessionHelper

class RequireLogin(cherrypy.Tool):

    def __init__(self):
        super(RequireLogin, self).__init__('before_handler', self.check, priority=49)
    
    def check(self, returnTo):
        cherrypy.log.error('inside check', 'RequireLogin')
        s = SessionHelper()
        if s.peek('user.account_id') is None:
            s.push('user.post_login_return_to', returnTo)
            raise cherrypy.HTTPRedirect('/error/login-required');
        
cherrypy.tools.require_login = RequireLogin()