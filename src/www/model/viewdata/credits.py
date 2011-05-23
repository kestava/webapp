
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
            'additionalMarkup': '<p>This is further based on Eric Meyer\'s \
<a href="http://meyerweb.com/eric/tools/css/reset/">Reset CSS</a>.</p>'
        },
        # Not using this yet, but hope to
        #{
        #    'name': 'Mark James',
        #    'description': '<p><a href="http://www.famfamfam.com/lab/icons/silk/">Silk icon set 1.3</a></p>'
        #}
        {
            'product': 'jQuery DataTables plugin',
            'productUrl': 'http://www.datatables.net/',
            'author': 'Allan Jardine',
            'authorUrl': 'http://www.sprymedia.co.uk/'
        }]
        
        return o
        