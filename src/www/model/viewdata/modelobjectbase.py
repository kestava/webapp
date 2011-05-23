
class ModelObjectBase(object):

    def read(self):
        raise NotImplementedError
        
    def __getattr__(self, name):
        if name == 'key':
            raise NotImplementedError("Child classes must provide a unique 'key' attribute.")
            
        raise AttributeError