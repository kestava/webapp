
import cherrypy
from jinja2 import Environment, FileSystemLoader

class SetupJinjaEnvironment(cherrypy.process.plugins.SimplePlugin):

    def __init__(self):
        super(SetupJinjaEnvironment, self).__init__(
            bus=cherrypy.engine)

    def start(self):
        """
        Set up the Jinja2 environment and attach it to the main
        application object.
        """
        app = cherrypy.tree.apps['']
        app.jinjaEnv = Environment(
            loader=FileSystemLoader(
                searchpath=app.config['appSettings']['jinja.search_path']))