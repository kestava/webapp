
from rawstringcomponent import RawStringComponent
from lib.xmlhelper import XmlHelper as xml

class StandardWarning(RawStringComponent):

    def __init__(self, paragraphData):
        super(StandardWarning, self).__init__(text=self.format_text(paragraphData))
        
    __markup = '''\
<section id="warningContainer">
{0}
</section>
'''
        
    def format_text(self, paragraphData):
        contents = []
        for i in paragraphData:
            e = xml.from_string(i)
            # Do any manipulations here
            xml.add_class(e, 'warningLine')
            contents.append(xml.to_string(e))
            
        return self.__markup.format('\n'.join(contents))