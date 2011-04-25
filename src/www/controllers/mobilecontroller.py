
import cherrypy

from mobiledynamiccontroller import MobileDynamicController

from model.userdatatheme import UserDataTheme
from model.userdata import UserData
from model.sitedata import SiteData

class MobileController(object):

    dynamic = MobileDynamicController()

    @cherrypy.tools.site_mode(mode='mobile')
    @cherrypy.tools.build_model(classes=[
        UserData,
        UserDataTheme,
        SiteData])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/mobile/root')
        return template.render(model=r.model)
        