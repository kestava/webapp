# _*_ coding: utf-8 _*_

import cherrypy

from lib.sitedata import SiteData
from lib.userdata import UserData
from dynamicfilescontroller import DynamicFilesController

class RootController(object):

    dynamic = DynamicFilesController()

    @cherrypy.expose
    def index(self):
        env = cherrypy.request.app.jinjaEnv
        u = UserData()
        templateName = 'html/{0}/homepage'.format(u.get_theme_name())
        template = env.get_template(templateName)
        return template.render(
            siteData=SiteData(),
            userData=u)