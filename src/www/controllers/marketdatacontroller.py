
import cherrypy

from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData
from model.viewdata.sitedata import SiteData

class MarketDataController(object):

    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/manage/market-data.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        