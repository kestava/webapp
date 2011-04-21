# _*_ coding: utf-8 _*_

import cherrypy

from logincontroller import LoginController
from lib.sessionhelper import SessionHelper

class AccountController(object):

    login = LoginController()
        
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