
import cherrypy

from modelobjectbase import ModelObjectBase

class SiteData(ModelObjectBase):
    
    key = 'siteData'
    
    def read(self):
        settings = cherrypy.request.app.config['appSettings']
        return {
            'siteName': settings['siteName'],
            'siteHostname': settings['siteHostname'],
            'html5ResetFilename': 'html5reset-1.6.1.css',
            'xrdsUrl': 'coming soon'
        }
        