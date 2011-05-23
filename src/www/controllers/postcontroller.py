
from pprint import pprint

import cherrypy

from model.viewdata.userdata import UserData
from model.viewdata.usersettings import UserSettings
from model.viewdata.sitedata import SiteData
from model.viewdata.itemdata import ItemData

from postmaterialcontroller import PostMaterialController

class PostController(object):
    
    material = PostMaterialController()
    
    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserData(),
        UserSettings()])
    @cherrypy.expose
    def transport(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/post/transport.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        