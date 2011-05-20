
from modelobjectbase import ModelObjectBase

class PageData(ModelObjectBase):
    """
    Serves as a generic placeholder for page-related data.  The controller can
    use this dictionary like::
    
        cherrypy.request.model['pageData']['someName'] = **some value**
    """
    
    key = 'pageData'
    
    def read(self):
        return {}