
import cherrypy

class SettingsHelper(object):

    def __init__(self):
        self.settings = cherrypy.request.app.config['appSettings']
    
    def cacheUserAgents(self):
        return 'cache.user_agents' in self.settings and \
            self.settings['cache.user_agents']