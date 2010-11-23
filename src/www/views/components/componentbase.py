
class ComponentBase(object):
    
    def output_to_stream(self, stream):
        raise NotImplementedError, 'Child classes should override ComponentBase.output_to_stream.'