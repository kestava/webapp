import pprint

import cherrypy

from controllerbase import ControllerBase
from views.login.loginpage import LoginPage

class LoginController(ControllerBase):
    
    def create_view(self):
        p = LoginPage()
        p.prepare()
        return p
        
    def before_create_view(self):
        if cherrypy.request.params.has_key('returnTo'):
            cherrypy.session['return-to-after-login'] = cherrypy.request.params['returnTo']