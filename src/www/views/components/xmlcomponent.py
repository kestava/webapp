import lxml

from componentbase import ComponentBase
from lib.xmlhelper import XmlHelper

class XmlComponent(ComponentBase):
    
    def __init__(self, tagname, attributes=None, text=None):
        super(XmlComponent, self).__init__()
        self.__root = XmlHelper.create_element(tagname=tagname, attributes=attributes, text=text)
    
    def output_to_stream(self, stream):
        print >> stream, XmlHelper.to_string(self.root, pretty_print=True)
        
    @property
    def root(self):
        return self.__root
    