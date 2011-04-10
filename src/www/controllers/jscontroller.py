
import cherrypy

from lib.sitedata import SiteData

class JsController(object):

    @cherrypy.expose(alias='app.js')
    def app(self):
        cherrypy.response.headers['content-type'] = 'application/javascript'
        env = cherrypy.request.app.jinjaEnv
        template = env.get_template('js/app')
        return template.render(siteData=SiteData())