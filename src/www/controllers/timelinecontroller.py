from controllerbase import ControllerBase
from views.timeline.publictimelinepage import PublicTimelinePage
class TimelineController(ControllerBase):
    
    def create_view(self):
        p = PublicTimelinePage()
        p.prepare()
        return p