from views.components.xmlcomponent import XmlComponent

class CentralContent(XmlComponent):
    
    def __init__(self):
        super(CentralContent, self).__init__(
            tagname='header')
        
        self.xml.create_subelement(
            parent=self.root,
            tagname='h1',
            text='kestava')