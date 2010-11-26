
from views.pagebase import PageBase
from views.components.rawstringcomponent import RawStringComponent
from lib.config import Config

class LoginPage(PageBase):
    
    __markup = '''\
<div id="contentContainer">
    <header>
        <h1><a href="/">Kestava</a></h1>
        <h2>Please select a provider to log in:</h2>
    </header>
    
    <form id="providersForm" method="post" action=".">
        <div id="providerSelectionsContainer">
            <!--<input id="chosenProvider" name="chosenProvider" type="hidden"/>-->
            <a id="providerGoogle" title="Google" class="largeButton provider Google"></a>
            <a id="providerYahoo" title="Yahoo!" class="largeButton provider Yahoo"></a>
        </div>
        
        <div id="providerInfoPanelContainer" style="display: none;">
            <div id="infoTextContainer">
            </div>
                
            <input id="providerSubmitButton" type="submit" class="formButton" value="Go"/>
            <input class="formButton cancelButton" type="button" value="Cancel"/>
            <input id="chosenProviderName" name="chosenProviderName" type="hidden"/>
        </div>
        
    </form>
</div>
'''
    
    def prepare(self):
        self._add_common_header_files()
        
        self.add_stylesheet('login.css')
        
        self.add_head_script('sprintf-0.7-beta1.js');
        
        if Config.get_environment() == 'development':
            self.add_head_script('login.js')
        else:
            self.add_head_script('login.min.js')
        
        self.add_page_component(RawStringComponent(self.__markup))