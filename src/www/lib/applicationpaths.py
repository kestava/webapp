
import urlparse

from lib import make_netloc

class ApplicationPaths(object):

    @classmethod
    def get_site_root(cls):
        return 'http://{0}/'.format(make_netloc())
        
    @classmethod
    def get_handle_openid_auth_response_path(cls):
        return urlparse.urljoin(cls.get_site_root(), 'account/login/openid/process')