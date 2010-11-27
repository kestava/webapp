
from viewbase import ViewBase
from lib.applicationpaths import ApplicationPaths

class XrdsView(ViewBase):
        
    __xrdsMarkup = '''\
<?xml version="1.0" encoding="UTF-8"?>
<xrds:XRDS
    xmlns:xrds="xri://$xrds"
    xmlns:openid="http://openid.net/xmlns/1.0"
    xmlns="xri://$xrd*($v*2.0)">
    <XRD>
        <Service priority="1">
            <Type>http://specs.openid.net/auth/2.0/return_to</Type>
            <URI>{0}</URI>
        </Service>
    </XRD>
</xrds:XRDS>
'''
        
    def prepare(self):
        self.headers['Content-Type'] = 'application/xrds+xml'
        
    def build_output(self):
        self.output = self.__xrdsMarkup.format(ApplicationPaths.get_handle_openid_auth_response_path())