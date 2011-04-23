
import cherrypy

from model.userdatatheme import UserDataTheme
from model.userdata import UserData
from model.sitedata import SiteData

class ConversationsController(object):

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserDataTheme,
        SiteData])
    @cherrypy.expose
    def users(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/users'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)
    
    @cherrypy.tools.build_model(classes=[
        UserData,
        UserDataTheme,
        SiteData])
    @cherrypy.expose
    def items(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/items'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)
        