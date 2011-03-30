from views.pagebase import PageBase

from views.components.standardpagenavlinks import StandardPageNavLinks
from views.components.standardpagetitlearea import StandardPageTitleArea
from publictimelineviewer import PublicTimelineViewer
from lib.config import Config

class PublicTimelinePage(PageBase):

    def prepare(self):
        self._add_common_header_files()
        self.add_stylesheet('public-timeline.css')
        
        # This needs to be a dynamic
        if Config.get_environment() == 'development':
            self.add_head_script('public-timeline.js')
        else:
            self.add_head_script('public-timeline.min.js')
        
        self.add_page_component(StandardPageNavLinks())
        self.add_page_component(StandardPageTitleArea(pageTitle="Public Timeline"))
        self.add_page_component(PublicTimelineViewer())
        
    def get_title(self):
        return '{0} | Public Timeline'.format(super(PublicTimelinePage, self).get_title())