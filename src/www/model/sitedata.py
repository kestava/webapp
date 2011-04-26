
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
        o['jQueryMobileCssUrl'] = '//code.jquery.com/mobile/1.0a4.1/jquery.mobile-1.0a4.1.css'
        o['jQueryMobileUrl'] = '//code.jquery.com/mobile/1.0a4.1/jquery.mobile-1.0a4.1.js'
        o['jQueryUrl'] = '//ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.js'
        o['jQueryUiUrl'] = '//ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.js'
        o['jQueryUiCssUrlTemplate'] = '//ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/%s/jquery-ui.css'
        
        return o