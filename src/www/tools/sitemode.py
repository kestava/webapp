
import logging

import cherrypy

class SiteMode(cherrypy.Tool):

    def __init__(self):
        super(SiteMode, self).__init__(
            'on_start_resource',
            self.set)
        
    def set(self, mode):
        req = cherrypy.request
        cherrypy.log.error('Inside set', 'SiteMode', severity=logging.DEBUG)
        req.siteMode = mode
        
cherrypy.tools.site_mode = SiteMode()
