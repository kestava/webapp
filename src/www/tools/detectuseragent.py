
import urllib
import urllib2
import json
import logging
from pprint import pprint, pformat

import cherrypy

class DetectUserAgent(cherrypy.Tool):

    def __init__(self):
        super(DetectUserAgent, self).__init__('before_handler', self.detect)
        
    def detect(self):
        req = cherrypy.request
        req.app.log.error('start', 'DetectUserAgent.detect',
            logging.DEBUG)
        
        settings = req.app.config['appSettings']
        hostname = settings['wurfl_service.host']
        port = settings['wurfl_service.port']
        ua = cherrypy.request.headers['user-agent']
        req.app.log.error(ua, 'DetectUserAgent.detect', logging.DEBUG)
        
        # make web service request URL
        percentEncoded = urllib.quote(ua, '')
        url = 'http://{0}:{1}/getUserAgentInfo?userAgentString={2}'.format(
            hostname, port, percentEncoded)
        req.app.log.error('URL: {0}'.format(url), 'DetectUserAgent.detect', logging.DEBUG)
        
        try:
            wsRequest = urllib2.urlopen(url)
            response = wsRequest.read()
            device = json.loads(response)
            req.userAgent = device
        except urllib2.URLError, er:
            req.app.log.error(str(er))

cherrypy.tools.detect_user_agent = DetectUserAgent()