# _*_ coding: utf-8 _*_

import cherrypy

from openidcontroller import OpenIDController
from lib.sitedata import SiteData
from lib.sessiondata import SessionData
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

    @cherrypy.expose
    def index(self):
        env = cherrypy.request.app.jinjaEnv
        u = SessionData()
        templateName = 'html/{0}/login/login-main'.format(u.get_theme_name())
        template = env.get_template(templateName)
        return template.render(
            siteData=SiteData(),
            sessionData=u)
        
    @cherrypy.expose
    def redirect(self, provider):
        redirectUrl = OpenIdHelper.get_auth_redirect_url(self.openIdProviders[provider]['url'])
        raise cherrypy.HTTPRedirect(redirectUrl)
        