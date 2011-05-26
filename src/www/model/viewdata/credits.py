
from modelobjectbase import ModelObjectBase

class Credits(ModelObjectBase):
    
    key = 'credits'
    
    def read(self):
        o = [
        {
            'product': 'html5doctor.com Reset Stylesheet',
            'productUrl': 'http://html5doctor.com/html-5-reset-stylesheet/',
            'author': 'Richard Clark',
            'authorUrl': 'http://richclarkdesign.com',
        },
        {
            'product': 'Silk icon set',
            'productUrl': 'http://www.famfamfam.com/lab/icons/silk/',
            'author': 'Mark James'
        },
        {
            'product': 'jQuery DataTables plugin',
            'productUrl': 'http://www.datatables.net/',
            'author': 'Allan Jardine',
            'authorUrl': 'http://www.sprymedia.co.uk/'
        }]
        
        return o
        