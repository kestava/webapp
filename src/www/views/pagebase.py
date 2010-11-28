import cStringIO
import pprint
import urlparse

import cherrypy

from viewbase import ViewBase
from lib.applicationpaths import ApplicationPaths
#import lib.config
import lib.xmlhelper
from lib.config import Config
import views.components.compositecomponent
from views.components.rawstringcomponent import RawStringComponent
import views.components.xmlcomponent

class PageBase(ViewBase):

    def __init__(self):
        super(PageBase, self).__init__()
        self._stylesheets = []
        self._headScripts = []
        self._pageComponents = []
        
        # Set default headers
        self.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.headers['X-XRDS-Location'] = urlparse.urljoin(ApplicationPaths.get_site_root(), '/xrds.xml')
            
    def _add_common_header_files(self):
        #config = lib.config.Config()
        config = cherrypy.request.app.config
        #pprint.pprint(config)
        
        self.add_stylesheet(config['appSettings']['html5ResetFilename'])
        self.add_stylesheet('base-style.css')
        
        if Config.get_environment() == 'development':
            self.add_head_script('kestava.js')
        else:
            self.add_head_script('kestava.min.js')
        
    def add_stylesheet(self, filename):
        self._stylesheets.append(filename)
        
    def get_stylesheets(self):
        return self._stylesheets
        
    def add_head_script(self, filename):
        self._headScripts.append(filename)
        
    def get_head_scripts(self):
        return self._headScripts
        
    def add_page_component(self, component):
        self._pageComponents.append(component)
        return component
        
    def get_page_components(self):
        return self._pageComponents
    
    def build_output(self):
        doc = views.components.compositecomponent.CompositeComponent()
        doc.add_component(views.components.rawstringcomponent.RawStringComponent(self.get_doctype()))
        html = doc.add_component(views.components.compositecomponent.CompositeComponent(tagname='html'))
        html.add_component(self.build_head())
        html.add_component(self.build_body())
    
        o = self.create_string_io()
        try:
            doc.output_to_stream(o)
            self.output = o.getvalue()
        finally:
            o.close()
    
    def create_string_io(self):
        return cStringIO.StringIO()
        
    def get_doctype(self):
        return '<!DOCTYPE html>'
        
    def get_title(self):
        return cherrypy.request.app.config['appSettings']['siteName']
    
    def build_head(self):
        head = views.components.compositecomponent.CompositeComponent(tagname='head')
        self.add_head_content(head)
        return head
        
    def build_body(self):
        body = views.components.compositecomponent.CompositeComponent(tagname='body')
        self.add_body_content(body)
        return body
        
    def add_body_content(self, body):
        c = views.components.compositecomponent.CompositeComponent(
            tagname='div',
            attributes={'id': 'mainContainer'})
        
        [c.add_component(i) for i in self._pageComponents]
        body.add_component(c)
        
    def add_head_content(self, head):
    
        def get_stylesheet_path(raw):
            return raw if raw.lower().startswith('http') \
                else '/css/{0}'.format(raw)
    
        head.add_component(views.components.rawstringcomponent.RawStringComponent('<title>{0}</title>'.format(self.get_title())))
        head.add_component(views.components.rawstringcomponent.RawStringComponent('<meta charset="UTF-8"/>'))
        
        stylesheets = (views.components.rawstringcomponent.RawStringComponent('<link rel="stylesheet" type="text/css" href="{0}"/>'.format(get_stylesheet_path(i))) for i in self._stylesheets)
        [head.add_component(i) for i in stylesheets]
        
        self.add_head_scripts(head)
        
    def add_head_scripts(self, head):
        htmlShiv = '''
<!--[if lt IE 9]>
<script type="text/javascript" src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
'''
        
        head.add_component(RawStringComponent(htmlShiv))
        head.add_component(RawStringComponent('<script type="text/javascript" src="{0}"></script>'.format(ApplicationPaths.paths['jquery'])))
        [head.add_component(RawStringComponent('<script type="text/javascript" src="{0}"></script>'.format(ApplicationPaths.get_script_path(i)))) \
            for i in self._headScripts]