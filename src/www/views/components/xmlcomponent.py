import lxml

from componentbase import ComponentBase
import lib.xmlhelper

class XmlComponent(ComponentBase):
    
    def __init__(self, tagname, attributes=None, text=None):
        super(XmlComponent, self).__init__()
        
        self.__xmlProvider = lib.xmlhelper.XmlHelper()
        self.__root = self.__xmlProvider.create_element(tagname=tagname, attributes=attributes, text=text)
    
    def output_to_stream(self, stream):
        print >> stream, lxml.etree.tostring(self.root, pretty_print=True)
        
    def get_xml_provider(self):
        return self.__xmlProvider
        
    xml = property(fget=get_xml_provider)
    
    def get_root_element(self):
        return self.__root
        
    root = property(fget=get_root_element)
    
    def add_class(self, className):
        self.xml.add_class(self.root, className)
    