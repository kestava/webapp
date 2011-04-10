# _*_ coding: utf-8 _*_

import cherrypy

from lib.sitedata import SiteData
from dynamicfilescontroller import DynamicFilesController

class RootController(object):

    dynamic = DynamicFilesController()

    @cherrypy.expose
    def index(self):
        env = cherrypy.request.app.jinjaEnv
        template = env.get_template('html/homepage')
        return template.render(siteData=SiteData())