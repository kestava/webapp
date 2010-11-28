import cherrypy

from controllers.logincontroller import LoginController
from views import create_view
from lib.openidhelper import OpenIdHelper
from openidpages import OpenIdPages

class LoginPages(object):

    openid = OpenIdPages()
    
    __openIdProviders = {
        'google': {
            'url': 'https://www.google.com/accounts/o8/id'
        },
        'yahoo': {
            'url': 'yahoo.com'
        }
    }

    @cherrypy.expose
    def index(self, **kwargs):
        if 'post' == cherrypy.request.method.lower():
            self.__handle_index_post(kwargs['chosenProviderName'])
        else:   
            c = LoginController()
            return create_view(c)
        
    def __handle_index_post(self, chosen):
        providerUrl = self.__openIdProviders[chosen]['url']
        redirectUrl = OpenIdHelper.get_auth_redirect_url(providerUrl)
        raise cherrypy.HTTPRedirect(redirectUrl)