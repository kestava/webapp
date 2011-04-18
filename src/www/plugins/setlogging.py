
from pprint import pformat
import logging

import cherrypy

class SetLogging(cherrypy.process.plugins.SimplePlugin):

    def __init__(self):
        super(SetLogging, self).__init__(bus=cherrypy.engine)
        
    def start(self):
        app = cherrypy.tree.apps['']
        logManager = app.log
        settings = app.config['appSettings']
        if 'logging.error_log.level' in settings:
            logManager.error_log.setLevel(settings['logging.error_log.level'])
            