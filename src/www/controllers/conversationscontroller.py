
import cherrypy

from model.usersettings import UserSettings
from model.userdata import UserData
from model.sitedata import SiteData

class ConversationsController(object):

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserSettings,
        SiteData])
    @cherrypy.expose
    def users(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/users.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
    
    @cherrypy.tools.build_model(classes=[
        UserData,
        UserSettings,
        SiteData])
    @cherrypy.expose
    def items(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/items.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        