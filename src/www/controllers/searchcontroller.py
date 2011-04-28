
import cherrypy

from model.usersettings import UserSettings
from model.userdata import UserData
from model.sitedata import SiteData

class SearchController(object):

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserSettings,
        SiteData])
    @cherrypy.expose
    def saved(object):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/search/saved.html'.format(r.model['userSettings']['themeName']))
        return template.render(model=r.model)