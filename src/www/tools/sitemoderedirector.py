
import logging

import cherrypy

class SiteModeRedirector(cherrypy.Tool):

    def __init__(self):
        super(SiteModeRedirector, self).__init__('before_request_body', self.run)
        
    def run(self):
        req = cherrypy.request
        cherrypy.log.error('Inside run', 'SiteModeRedirector', logging.DEBUG)
        
        userSiteMode = 'web'
        if 'user.site_mode' in cherrypy.session:
            userSiteMode = cherrypy.session.get('user.site_mode')
        else:
            if req.userAgentInfo.isWirelessDevice and \
                not req.userAgentInfo.isTablet:
                userSiteMode = 'mobile'
        
        pageSiteMode = req.siteMode if hasattr(req, 'siteMode') else 'web'
        
        cherrypy.log.error('User Site Mode: {0}'.format(userSiteMode),
            'SiteModeRedirector')
        cherrypy.log.error('Page Site Mode: {0}'.format(pageSiteMode),
            'SiteModeRedirector')
        
        if 'any' != pageSiteMode:
            if 'mobile' == userSiteMode and 'mobile' != pageSiteMode:
                cherrypy.log.error('Redirecting user to the mobile site',
                    'SiteModeRedirector')
                raise cherrypy.HTTPRedirect('/mobile')
        
cherrypy.tools.site_mode_redirector = SiteModeRedirector()
