import pprint

import cherrypy

class RequestDebugging(cherrypy.Tool):
    
    def __init__(self):
        super(RequestDebugging, self).__init__('on_start_resource', self.__debug)
        
    def __debug(self):
        pass
        #print('Inside RequestDebugging.__debug')
        #request = cherrypy.request
        #print(dir(request))
        #pprint.pprint(request.headers)
        
                        
cherrypy.tools.request_debugging = RequestDebugging()