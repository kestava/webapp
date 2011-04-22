
import logging
from pprint import pprint, pformat

import cherrypy

from lib.useragentinfo import UserAgentInfo

class DetectUserAgent(cherrypy.Tool):

    def __init__(self):
        super(DetectUserAgent, self).__init__('before_handler', self.detect)
        
    def detect(self):
        req = cherrypy.request
        ua = req.headers['user-agent']
        info = UserAgentInfo.from_cache(ua)
        req.userAgentInfo = UserAgentInfo.from_web_service(ua) if info is None else info
        req.app.log.error('Is tablet: {0}'.format(req.userAgentInfo.isTablet))
        req.app.log.error('Is wireless device: {0}'.format(req.userAgentInfo.isWirelessDevice))
        
cherrypy.tools.detect_user_agent = DetectUserAgent()
