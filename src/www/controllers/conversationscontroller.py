
import cherrypy

from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData
from model.viewdata.sitedata import SiteData

class ConversationsController(object):

    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def users(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/users.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
    
    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def items(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/conversations/items.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        