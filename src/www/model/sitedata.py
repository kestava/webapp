
import cherrypy

from modelobjectbase import ModelObjectBase

class SiteData(ModelObjectBase):
    
    key = 'siteData'
    
    def read(self):
        settings = cherrypy.request.app.config['appSettings']
        
        o = {
            'siteName': settings['siteName'],
            'siteHostname': settings['siteHostname'],
            'html5ResetFilename': 'html5reset-1.6.1.css',
            'xrdsUrl': 'coming soon'
        }
        
        # TODO: set these based on configuration (use CDN or not, minified or
        # non-minified, etc.)
        o['jQueryMobileCssUrl'] = 'http://code.jquery.com/mobile/1.0a4.1/jquery.mobile-1.0a4.1.css'
        o['jQueryMobileUrl'] = 'http://code.jquery.com/mobile/1.0a4.1/jquery.mobile-1.0a4.1.js'
        o['jQueryUrl'] = 'http://code.jquery.com/jquery-1.5.2.js'
        
        return o