
from controllerbase import ControllerBase
from views.xrdsview import XrdsView

class XrdsController(ControllerBase):
    
    def create_view(self):
        v = XrdsView()
        v.prepare()
        return v