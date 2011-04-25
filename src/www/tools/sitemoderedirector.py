
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
            if req.userAgentInfo.isWirelessDevice:
                userSiteMode = 'mobile'
        
        pageSiteMode = req.siteMode if hasattr(req, 'siteMode') else 'web'
        
        print('User Site Mode: {0}'.format(userSiteMode))
        print('Page Site Mode: {0}'.format(pageSiteMode))
        
        if 'any' != pageSiteMode:
            if 'mobile' == userSiteMode and 'mobile' != pageSiteMode:
                cherrypy.log.error('Redirecting user to the mobile site',
                    'SiteModeRedirector')
                raise cherrypy.HTTPRedirect('/mobile')
        
cherrypy.tools.site_mode_redirector = SiteModeRedirector()
