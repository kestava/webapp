# _*_ coding: utf-8 _*_

import cherrypy

from lib.sitedata import SiteData
from lib.sessiondata import SessionData
from dynamicfilescontroller import DynamicFilesController
from logincontroller import LoginController

class RootController(object):

    dynamic = DynamicFilesController()
    login = LoginController()

    @cherrypy.expose
    def index(self):
        env = cherrypy.request.app.jinjaEnv
        u = SessionData()
        templateName = 'html/{0}/homepage'.format(u.get_theme_name())
        template = env.get_template(templateName)
        return template.render(
            siteData=SiteData(),
            sessionData=u)