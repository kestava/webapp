
from pprint import pprint

import cherrypy

from model.userdata import UserData
from model.usersettings import UserSettings
from model.sitedata import SiteData
from model.itemdata import ItemData

class PostMaterialController(object):

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
        pprint(r.model)
        return template.render(model=r.model)
        
    @cherrypy.expose
    def create(self):
        return 'create'