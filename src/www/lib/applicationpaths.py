from lib.config import Config

class ApplicationPaths(object):
    
    class PathsDescr(object):
        def __get__(self, instance, owner):
            def get_jquery_filename():
                return 'jquery-1.4.4.js' \
                    if 'development' == Config.get_environment() \
                    else 'jquery-1.4.4.min.js'
                
            return {
                'jquery': '/js/' + get_jquery_filename()
            }
    
    paths = PathsDescr()
    
    @classmethod
    def get_script_path(cls, filename):
        return '/js/' + filename
    
    @classmethod    
    def get_secure_site_root(cls):
        config = lib.config.Config()
        return 'https://{0}/'.format(config.hostName)