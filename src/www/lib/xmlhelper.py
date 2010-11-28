import lxml.etree

class XmlHelper(object):
    
    @classmethod
    def create_element(cls, tagname, attributes=None, text=None):
        o = lxml.etree.Element(tagname)
        cls.__set_attributes(o, attributes, text)
        return o
    
    @classmethod
    def create_subelement(cls, parent, tagname, attributes=None, text=None, tail=None):
        o = lxml.etree.SubElement(parent, tagname)
        cls.__set_attributes(o, attributes, text, tail)
        return o
        
    @classmethod
    def __set_attributes(cls, element, attributes=None, text=None, tail=None):
        if not attributes is None:
            for i in attributes:
                element.set(i, attributes[i])
            
        if not text is None:
            element.text = text
            
        if not tail is None:
            element.tail = tail

    @classmethod
    def add_class(cls, element, classname):
        c = element.get('class')
        
        if c is None:
            element.set('class', classname)
        else:
            # see if the classname is already listed
            parts = c.split()
            if not classname in parts:
                parts.append(classname)
                element.set('class', ' '.join(parts))
                
    @classmethod
    def remove_class(cls, element, classname):
        c = element.get('class')
        
        if not c is None:
            # if the class name exists in the class string, remove it
            parts = c.split()
            if classname in parts:
                parts.remove(classname)
                element.set('class', ' '.join(parts))
        
    @classmethod
    def from_string(cls, source):
        return lxml.etree.fromstringlist(source.splitlines())
        
    @classmethod
    def to_string(cls, element, pretty_print=False):
        return lxml.etree.tostring(element, pretty_print=pretty_print)