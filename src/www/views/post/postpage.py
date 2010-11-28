import cherrypy

from views.pagebase import PageBase
from views.components.standardpagenavlinks import StandardPageNavLinks
from views.components.standardpagetitlearea import StandardPageTitleArea
from postitemform import PostItemForm
from views.components.compositecomponent import CompositeComponent
from views.components.standardwarning import StandardWarning

class PostPage(PageBase):

    def prepare(self):
        self._add_common_header_files()
        self.add_stylesheet('post.css')
        
        self.add_page_component(StandardPageNavLinks(returnToAfterLogin='/post'))
        self.add_page_component(StandardPageTitleArea(pageTitle='Post Item'))
        
        c = CompositeComponent(
            tagname='div',
            attributes={'id': 'postItemFormContainer'})
        
        if cherrypy.session.has_key('account-id'):
            c.add_component(PostItemForm())
        else:
            c.add_component(StandardWarning(self.__loginWarningData))
        
        self.add_page_component(c)
        
    __loginWarningData = ['<h1>Login required</h1>', '<p>Please <a href="/login?returnTo=/post">login</a> to post.</p>']
        
    def get_title(self):
        return '{0} | Post Item'.format(super(PostPage, self).get_title())