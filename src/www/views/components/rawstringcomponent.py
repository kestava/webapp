from componentbase import ComponentBase

class RawStringComponent(ComponentBase):

    def __init__(self, text):
        super(RawStringComponent, self).__init__()
        self.__text = text
        
    def output_to_stream(self, stream):
        print >> stream, self.__text

