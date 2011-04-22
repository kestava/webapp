
import urllib
import urllib2
import json
from pprint import pprint

import cherrypy

class UserAgentInfo(object):

    cacheName = 'userAgentInfoCache'

    def __init__(self, deviceInfo):
    
        # Add support for new device caps by adding to this array
        a = [('product_info', 'is_tablet', '_UserAgentInfo__isTablet'),
            ('product_info', 'is_wireless_device', '_UserAgentInfo__isWirelessDevice')]
    
        # product info
        #pprint(deviceInfo)
        
        for i in a:
            group = i[0]
            property = i[1]
            localAttribute = i[2]
            
            setattr(
                self,
                localAttribute,
                deviceInfo[group][property] \
                    if group in deviceInfo and property in deviceInfo[group] \
                    else None)
        
    @property
    def isTablet(self):
        return self.__isTablet
    
    @property
    def isWirelessDevice(self):
        return self.__isWirelessDevice
        
    @classmethod
    def from_cache(cls, userAgentString):
        app = cherrypy.request.app
        if hasattr(app, cls.cacheName):
            temp = getattr(app, cls.cacheName)
            if userAgentString in temp:
                print('Returning user agent info from cache')
                return temp[userAgentString]
                
    @classmethod
    def from_web_service(cls, userAgentString):
        req = cherrypy.request
        settings = req.app.config['appSettings']
        hostname = settings['wurfl_service.host']
        port = settings['wurfl_service.port']
        
        # make web service request URL
        percentEncoded = urllib.quote(userAgentString, '')
        url = 'http://{0}:{1}/getUserAgentInfo?userAgentString={2}'.format(
            hostname, port, percentEncoded)
        
        try:
            wsRequest = urllib2.urlopen(url)
            response = wsRequest.read()
            info = UserAgentInfo(json.loads(response))
            cls.cache_info(userAgentString, info)
            return info
        except urllib2.URLError, er:
            req.app.log.error(str(er))
            return NullUserAgentInfo()
            
    @classmethod
    def cache_info(cls, userAgentString, userAgentInfo):
        app = cherrypy.request.app
        if not hasattr(app, cls.cacheName):
            setattr(app, cls.cacheName, {})
        temp = getattr(app, cls.cacheName)
        temp[userAgentString] = userAgentInfo
            
class NullUserAgentInfo(UserAgentInfo):
    
    def __init__(self):
        super(NullUserAgentInfo, self).__init__({})
        