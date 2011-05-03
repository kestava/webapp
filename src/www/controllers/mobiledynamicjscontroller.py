
import cherrypy

from model.sitedata import SiteData

class MobileDynamicJsController(object):

    @cherrypy.tools.site_mode(mode='mobile')
    @cherrypy.tools.build_model(includes=[SiteData()])
    @cherrypy.expose(alias='app.js')
    def app(self):
        req = cherrypy.request
        cherrypy.response.headers['content-type'] = 'application/javascript'
        template = req.app.jinjaEnv.get_template('js/app.js')
        return template.render(model=req.model)