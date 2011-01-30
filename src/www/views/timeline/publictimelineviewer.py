from views.components.xmlcomponent import XmlComponent
from lib.xmlhelper import XmlHelper as xml

class PublicTimelineViewer(XmlComponent):
    
    def __init__(self):
        super(PublicTimelineViewer, self).__init__(
            tagname='section')
        
        self.root.set('id', 'timelineContainer')
        
        temp = xml.create_subelement(
            parent=self.root,
            tagname='div')
        
        xml.add_class(temp, 'innerContainer')
        
        