from componentbase import ComponentBase

class CompositeComponent(ComponentBase):

    def __init__(self, tagname=None, attributes=None):
        super(CompositeComponent, self).__init__()
        self.__tagname = tagname
        self.__attributes = attributes
        self.__components = []
        
    def output_to_stream(self, stream):
        openingTag = self.get_opening_tag()
        if not openingTag is None:
            print >> stream, openingTag
            
        for i in self.__components:
            i.output_to_stream(stream)
            
        closingTag = self.get_closing_tag()
        if not closingTag is None:
            print >> stream, closingTag
        
    def add_component(self, component):
        self.__components.append(component)
        return component
        
    def get_opening_tag(self):
        if self.__tagname is None:
            return None
            
        if self.__attributes is None or 1 > len(self.__attributes):
            a = ''
        else:
            g = ('{0}="{1}"'.format(i, self.__attributes[i]) for i in self.__attributes)
            a = ' ' + ' '.join(g)
            
        return '<{0}{1}>'.format(self.__tagname, a)
        
    def get_closing_tag(self):
        if self.__tagname is None:
            return None
            
        return '</{0}>'.format(self.__tagname)