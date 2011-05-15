
from pprint import pprint, pformat

import cherrypy
from setproctitle import setproctitle

class SetProcessTitle(cherrypy.process.plugins.SimplePlugin):

    def __init__(self):
        super(SetProcessTitle, self).__init__(bus=cherrypy.engine)
        
    def start(self):
        app = cherrypy.tree.apps['']
        port = app.config['global']['server.socket_port']
        setproctitle('unsilo-webapp-{0}'.format(port))