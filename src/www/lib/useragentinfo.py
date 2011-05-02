
import urllib
import urllib2
import json
import logging
from pprint import pprint

import cherrypy

from lib.settingshelper import SettingsHelper

class UserAgentInfo(object):

    cacheName = 'userAgentInfoCache'

    def __init__(self, deviceInfo):
        
        self.__id = deviceInfo['device_id']
        self.__userAgent = deviceInfo['device_ua']
    
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
    def id(self):
        return self.__id
        
    @property
    def userAgent(self):
        return self.__userAgent
    
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
                cherrypy.log.error(
                    'from_cache returning user agent info from cache',
                    'UserAgentInfo',
                    logging.DEBUG)
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
            if SettingsHelper().cacheUserAgents():
                cls.cache_info(userAgentString, info)
            return info
        except urllib2.URLError, er:
            cherrypy.log.error(str(er), 'UserAgentInfo.from_web_service')
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
        