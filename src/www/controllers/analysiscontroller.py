
import cherrypy

from model.userdatatheme import UserDataTheme
from model.userdata import UserData
from model.sitedata import SiteData

class AnalysisController(object):

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserDataTheme,
        SiteData])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/manage/analysis'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)