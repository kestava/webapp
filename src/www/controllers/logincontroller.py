
from controllerbase import ControllerBase
from views.login.loginpage import LoginPage

class LoginController(ControllerBase):
    
    def create_view(self):
        p = LoginPage()
        p.prepare()
        return p