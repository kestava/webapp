from views.components.xmlcomponent import XmlComponent
from lib.xmlhelper import XmlHelper as xml

class CentralContent(XmlComponent):
    
    def __init__(self):
        super(CentralContent, self).__init__(
            tagname='header')
        
        xml.create_subelement(
            parent=self.root,
            tagname='h1',
            text='kestava')