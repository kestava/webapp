# _*_ coding: utf-8 _*_

import cherrypy

from lib.sitedata import SiteData
from lib.sessiondata import SessionData
from dynamicfilescontroller import DynamicFilesController
from logincontroller import LoginController
from errorcontroller import ErrorController

class RootController(object):

    dynamic = DynamicFilesController()
    login = LoginController()
    error = ErrorController()

    @cherrypy.expose
    def index(self):
        env = cherrypy.request.app.jinjaEnv
        u = SessionData()
        templateName = 'html/{0}/homepage'.format(u.get_theme_name())
        template = env.get_template(templateName)
        return template.render(
            siteData=SiteData(),
            sessionData=u)
    
    @cherrypy.expose(alias='xrds.xml')
    def handle_xrds(self):
        # TODO: Create a tool to add the following response header pointing to
        # this document:
        # cherrypy.response.headers['X-XRDS-Location']
        
        cherrypy.response.headers['content-type'] = 'application/xrds+xml'
        env = cherrypy.request.app.jinjaEnv
        template = env.get_template('html/misc/xrds')
        return template.render(siteData=SiteData())