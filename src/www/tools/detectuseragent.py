
import logging
from pprint import pprint, pformat

import cherrypy

from wurfl import devices
from pywurfl.algorithms import TwoStepAnalysis

class DetectUserAgent(cherrypy.Tool):

    def __init__(self):
        super(DetectUserAgent, self).__init__('before_handler', self.detect)
        
    def detect(self):
        cherrypy.request.app.log.error('start', 'DetectUserAgent.detect',
            logging.DEBUG)
        
        ua = cherrypy.request.headers['user-agent']
        cherrypy.request.app.log.error('UA string: {0}'.format(ua),
            'DetectUserAgent.detect', logging.DEBUG)
        
        search_algorithm = TwoStepAnalysis(devices)
        device = devices.select_ua(
            unicode(ua),
            search=search_algorithm)
        
        cherrypy.request.userAgent = device

cherrypy.tools.detect_user_agent = DetectUserAgent()