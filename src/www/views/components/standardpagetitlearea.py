
from xmlcomponent import XmlComponent
from lib.xmlhelper import XmlHelper as xml

class StandardPageTitleArea(XmlComponent):
    
    def __init__(self, pageTitle):
        super(StandardPageTitleArea, self).__init__(tagname='header')
        
        self.root.set('id', 'standardTitleContainer')
        
        xml.create_subelement(
            parent=xml.create_subelement(
                parent=self.root,
                tagname='h1'),
            tagname='a',
            attributes={'href': '/'},
            text='Kestava')
        
        xml.create_subelement(
            parent=self.root,
            tagname='hr')
        
        xml.create_subelement(
            parent=self.root,
            tagname='h2',
            text=pageTitle)
        
        

