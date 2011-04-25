
import cherrypy

class SiteModeRedirector(cherrypy.Tool):

    def __init__(self):
        super(SiteModeRedirector, self).__init__('before_request_body', self.run)
        
    def run(self):
        req = cherrypy.request
        req.app.log.error('Inside run', 'SiteModeRedirector')
        
        #userSiteMode = cherrypy.session.get('user.site_mode') \
        #    if 'user.site_mode' in cherrypy.session \
        #    else 'web'
        
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
                req.app.log.error('Redirecting user to the mobile site',
                    'SiteModeRedirector')
                raise cherrypy.HTTPRedirect('/mobile')
        
cherrypy.tools.site_mode_redirector = SiteModeRedirector()
