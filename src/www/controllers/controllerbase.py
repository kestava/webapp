
class ControllerBase(object):

    def __init__(self):
        self.__args = {}
        
    @property
    def args(self):
        return self.__args
        
    def before_create_view(self):
        pass
        
    def after_create_view(self):
        pass