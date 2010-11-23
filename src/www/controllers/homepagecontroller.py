

from controllerbase import ControllerBase
from views.homepage.homepagepage import HomepagePage

class HomePageController(ControllerBase):
    
    def create_view(self):
        view = HomepagePage()
        view.prepare()
        return view