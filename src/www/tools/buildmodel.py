
import cherrypy

from model import load_model

class BuildModel(cherrypy.Tool):
    
    def __init__(self):
        super(BuildModel, self).__init__('before_handler', self.build)
        
    def build(self, includes):
        """
        Build up a model object and attach it to the request object.
        
        The goal is that all database activity will be concentrated here.
        """
        cherrypy.request.model = load_model(includes)
        
cherrypy.tools.build_model = BuildModel()