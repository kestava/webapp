
import cherrypy

# tools
import tools.connectdb

from config import config
from controllers.rootcontroller import RootController
from plugins.setupjinjaenvironment import SetupJinjaEnvironment

def configure():
    o = {}
    o.update(config)
    return o
    
def main():
    
    SetupJinjaEnvironment().subscribe()
    
    cherrypy.quickstart(
        root=RootController(),
        config=configure()
    )
    
if __name__ == '__main__':
    main()