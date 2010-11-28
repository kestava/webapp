
from views.components.rawstringcomponent import RawStringComponent

class PostItemForm(RawStringComponent):

    def __init__(self):
        super(PostItemForm, self).__init__(text=self.format_text())
        
    __formMarkup = '''\
<form method="POST" action="/post">
    <div>
        <input type="submit" value="Post Item"/>
    </div>
</form>
'''
        
    def format_text(self):
        return self.__formMarkup