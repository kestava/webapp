
import cherrypy

from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData
from model.viewdata.sitedata import SiteData

class SearchController(object):

    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def saved(object):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/search/saved.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)