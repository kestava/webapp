
import cherrypy

from model.userdata import UserData
from model.userdatatheme import UserDataTheme
from model.sitedata import SiteData

class PostController(object):

    @cherrypy.tools.build_model(classes=[
        SiteData,
        UserData,
        UserDataTheme])
    @cherrypy.expose
    def material(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/material'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)
        
    @cherrypy.tools.build_model(classes=[
        SiteData,
        UserData,
        UserDataTheme])
    @cherrypy.expose
    def transport(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/transport'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)
        