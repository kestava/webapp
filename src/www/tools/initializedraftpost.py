
import cherrypy

from model.itemdata import ItemData
from lib.sessionhelper import SessionHelper

class InitializeDraftPost(cherrypy.Tool):

    def __init__(self):
        super(InitializeDraftPost, self).__init__(
            'before_handler',
            self.initialize,
            priority=49)
        
    def initialize(self):
        """
        If there is no posted item in draft status for the current user,
        create one
        """
        id = SessionHelper().peek('user.account_id')
        if not ItemData.user_has_draft_item(id): ItemData.create_user_draft_item(id)
        
cherrypy.tools.initialize_draft_post = InitializeDraftPost()
