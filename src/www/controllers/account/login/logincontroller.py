
import cherrypy

from controllers.account.login.openid import OpenIDController
from model.usersettings import UserSettings
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

    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserSettings()])
    @cherrypy.expose
    def index(self):
        req = cherrypy.request
        template = req.app.jinjaEnv.get_template('html/{0}/login/login-main.html'.format(req.model['userSettings']['layout']))
        return template.render(model=req.model)
        
    @cherrypy.expose
    def redirect(self, provider):
        redirectUrl = OpenIdHelper.get_auth_redirect_url(self.openIdProviders[provider]['url'])
        raise cherrypy.HTTPRedirect(redirectUrl)