
import cherrypy

from model.sitedata import SiteData

class JsController(object):

    @cherrypy.tools.build_model(classes=[SiteData])
    @cherrypy.expose(alias='app.js')
    def app(self):
        req = cherrypy.request
        cherrypy.response.headers['content-type'] = 'application/javascript'
        template = req.app.jinjaEnv.get_template('js/app')
        return template.render(model=req.model)