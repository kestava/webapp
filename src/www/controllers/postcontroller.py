
from controllerbase import ControllerBase
from views.post.postpage import PostPage

class PostController(ControllerBase):

    def create_view(self):
        p = PostPage()
        p.prepare()
        return p