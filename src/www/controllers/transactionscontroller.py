
import cherrypy

from model.usersettings import UserSettings
from model.userdata import UserData
from model.sitedata import SiteData

class TransactionsController(object):

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserSettings,
        SiteData])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/manage/transactions.html'.format(r.model['userSettings']['themeName']))
        return template.render(model=r.model)
        