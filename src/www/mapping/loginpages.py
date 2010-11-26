import cherrypy

from controllers.logincontroller import LoginController
from views.viewcreator import ViewCreator
from lib.openidhelper import OpenIdHelper
from openidpages import OpenIdPages

class LoginPages(object):

    openid = OpenIdPages()

    @cherrypy.expose
    def index(self, **kwargs):
        if 'post' == cherrypy.request.method.lower():
            self.__handle_index_post(kwargs['chosenProviderName'])
        else:
            c = LoginController()
            return ViewCreator.create_view(c)
        
    def __handle_index_post(self, chosen):
        providerUrl = None
        
        if 'google' == chosen:
            providerUrl = 'https://www.google.com/accounts/o8/id'
            
        redirectUrl = OpenIdHelper.get_auth_redirect_url(providerUrl)
        raise cherrypy.HTTPRedirect(redirectUrl)