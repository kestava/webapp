
import cherrypy

from controllers.account.login.openid.openidcontroller import OpenIDController
from model.viewdata.usersettings import UserSettings
from model.viewdata.sitedata import SiteData
from model.viewdata.authenticationproviders import AuthenticationProviders
from lib.openidhelper import OpenIdHelper

class LoginController(object):

    openid = OpenIDController()

    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserSettings(),
        AuthenticationProviders()])
    @cherrypy.expose
    def index(self):
        req = cherrypy.request
        template = req.app.jinjaEnv.get_template('html/{0}/login/login-main.html'.format(req.model['userSettings']['layout']))
        return template.render(model=req.model)
        
    @cherrypy.expose
    def redirect(self, provider, authType, authUrl):
        if authType == 'openid':
            redirectUrl = OpenIdHelper.get_auth_redirect_url(authUrl)
        else:
            raise NotImplementedError()
            
        raise cherrypy.HTTPRedirect(redirectUrl)