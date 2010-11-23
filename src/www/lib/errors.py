class ApplicationError(Exception):
    
    def __init__(self, message):
        self.__message = message
    
    @property    
    def message(self):
        return self.__message

class NotImplementedError(ApplicationError):
    
    def __init__(self, codeDescr):
        t = 'Not Implemented: {0}'.format(codeDescr)
        super(NotImplementedError, self).__init__(t)