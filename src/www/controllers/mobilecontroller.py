
import cherrypy

from mobiledynamiccontroller import MobileDynamicController

from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData
from model.viewdata.sitedata import SiteData

class MobileController(object):

    dynamic = MobileDynamicController()

    @cherrypy.tools.site_mode(mode='mobile')
    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/mobile/root.html')
        return template.render(model=r.model)
        