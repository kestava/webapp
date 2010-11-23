import lxml.etree

class XmlHelper(object):
    
    def create_element(self, tagname, attributes=None, text=None):
        o = lxml.etree.Element(tagname)
        self.__set_attributes(o, attributes, text)
        return o
    
    def create_subelement(self, parent, tagname, attributes=None, text=None, tail=None):
        o = lxml.etree.SubElement(parent, tagname)
        self.__set_attributes(o, attributes, text, tail)
        return o
        
    def __set_attributes(self, element, attributes=None, text=None, tail=None):
        if not attributes is None:
            for i in attributes:
                element.set(i, attributes[i])
            
        if not text is None:
            element.text = text
            
        if not tail is None:
            element.tail = tail

    def add_class(self, element, classname):
        c = element.get('class')
        
        if c is None:
            element.set('class', classname)
        else:
            # see if the classname is already listed
            parts = c.split()
            if not classname in parts:
                parts.append(classname)
                element.set('class', ' '.join(parts))
                
    def remove_class(self, element, classname):
        c = element.get('class')
        
        if not c is None:
            # if the class name exists in the class string, remove it
            parts = c.split()
            if classname in parts:
                parts.remove(classname)
                element.set('class', ' '.join(parts))
        
    def from_string(self, source):
        return lxml.etree.fromstringlist(source.splitlines())
    
    def set_attribute(self, element, attribute, value):
        element.set(attribute, value)