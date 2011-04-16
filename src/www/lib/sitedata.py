
import cherrypy

class SiteData(object):

    def __init__(self):
        self.xrdsUrl = 'blah'

    def __getattr__(self, name):
        
        if name in cherrypy.request.app.config['appSettings']:
            return cherrypy.request.app.config['appSettings'][name]
            
        raise AttributeError()
        