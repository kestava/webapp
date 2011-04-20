
import cherrypy

from openidcontroller import OpenIDController
from model.userdatatheme import UserDataTheme
from model.sitedata import SiteData
from lib.openidhelper import OpenIdHelper

class LoginController(object):

    openid = OpenIDController()

    openIdProviders = {
        'google': {
            'url': 'https://www.google.com/accounts/o8/id'
        },
        'yahoo': {
            'url': 'yahoo.com'
        }
    }

    @cherrypy.tools.build_model(classes=[
        SiteData,
        UserDataTheme])
    @cherrypy.expose
    def index(self):
        req = cherrypy.request
        template = req.app.jinjaEnv.get_template('html/{0}/login/login-main'.format(req.model['userData']['themeName']))
        return template.render(model=req.model)
        
    @cherrypy.expose
    def redirect(self, provider):
        redirectUrl = OpenIdHelper.get_auth_redirect_url(self.openIdProviders[provider]['url'])
        raise cherrypy.HTTPRedirect(redirectUrl)