
from pprint import pprint

import cherrypy

from model.viewdata.userdata import UserData
from model.viewdata.usersettings import UserSettings
from model.viewdata.sitedata import SiteData
from model.viewdata.itemdata import ItemData

class PostMaterialController(object):

    @cherrypy.tools.require_login(returnTo='/post/material')
    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserData(),
        UserSettings(),
        ItemData('userItemsAll')])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/material.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        
    @cherrypy.tools.initialize_draft_post()
    @cherrypy.expose
    def create(self):
        return 'create'