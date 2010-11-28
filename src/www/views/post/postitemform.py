
from views.components.rawstringcomponent import RawStringComponent

class PostItemForm(RawStringComponent):

    def __init__(self):
        super(PostItemForm, self).__init__(text=self.format_text())
        
    __formMarkup = '''\
<form id="postItemForm" method="POST" action="/post">
    <div>
        <div class="formRow">
            <label for="shortDescription">Description</label>
            <input id="shortDescription" name="shortDescription" class="niceInput"/>
        </div>
        
        <fieldset id="locationRow">
            <legend style="display: none">Location</legend>
            
            <div class="formRow">
                <label for="lookupAddress">Address</label>
                <input id="lookupAddress" name="lookupAddress" class="niceInput"/>
                <button>Select</button>
            </div>
            
            <div class="formRow">
                <label for="longLat">Longitude, Latitude</label>
                <input id="longLat" name="exactLongLat" class="niceInput"/>
                <button>Select</button>
                <em id="toggleMap" class="closed">Locate on map</em>
            </div>
        </fieldset>
        
        <input type="submit" value="Post Item"/>
    </div>
</form>
'''
        
    def format_text(self):
        return self.__formMarkup