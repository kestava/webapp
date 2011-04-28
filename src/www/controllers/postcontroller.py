
import cherrypy

from model.userdata import UserData
from model.usersettings import UserSettings
from model.sitedata import SiteData

class PostController(object):

    @cherrypy.tools.build_model(classes=[
        SiteData,
        UserData,
        UserSettings])
    @cherrypy.expose
    def material(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/material.html'.format(r.model['userSettings']['themeName']))
        return template.render(model=r.model)
        
    @cherrypy.tools.build_model(classes=[
        SiteData,
        UserData,
        UserSettings])
    @cherrypy.expose
    def transport(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/transport.html'.format(r.model['userSettings']['themeName']))
        return template.render(model=r.model)
        