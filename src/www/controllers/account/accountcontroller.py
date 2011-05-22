
import cherrypy

from login.logincontroller import LoginController
from createcontroller import CreateController
from addcontroller import AddController
from lib.sessionhelper import SessionHelper

class AccountController(object):
    
    login = LoginController()
    create = CreateController()
    add = AddController()
    
    @cherrypy.expose
    def logout(self):
        """
        Remove any user data from the session and redirect to the page that
        the user was viewing previously.
        """
        returnTo = cherrypy.session.get('user.return_to_path')
        returnTo = '/' if returnTo is None or '' == returnTo else returnTo
        
        SessionHelper().clear_user_data()
        
        raise cherrypy.HTTPRedirect(returnTo)
        
    @cherrypy.expose
    def profile(self):
        return 'profile'
        
    @cherrypy.expose
    def settings(self):
        return 'settings'