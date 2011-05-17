
import cherrypy
from jinja2 import Environment, FileSystemLoader

class SetupJinjaEnvironment(cherrypy.process.plugins.SimplePlugin):

    def __init__(self):
        super(SetupJinjaEnvironment, self).__init__(
            bus=cherrypy.engine)
        
    def guess_autoescape(self, template_name):
        if template_name is None or '.' not in template_name:
            return False
        ext = template_name.rsplit('.', 1)[1]
        return ext in ('html', 'xml')

    def start(self):
        """
        Set up the Jinja2 environment and attach it to the main
        application object.
        """
        app = cherrypy.tree.apps['']
        app.jinjaEnv = Environment(
            loader=FileSystemLoader(
                searchpath=app.config['appSettings']['jinja.search_path']),
            autoescape=self.guess_autoescape,
            extensions=['jinja2.ext.autoescape'])
        