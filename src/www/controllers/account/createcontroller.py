
import cherrypy

from model.userdata import UserData
from model.usersettings import UserSettings
from model.sitedata import SiteData
from lib.sessionhelper import SessionHelper

class CreateController(object):
    
    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def index(self):
        """
        .. note:: An OpenID Identifier must be present in the user's session data.
        """
        r = cherrypy.request
        s = SessionHelper()
        k = 'account_create.openid_identity_url'
        if not s.has_key(k):
            raise cherrypy.HTTPError(400, message='Missing OpenID identity')
            
        # Permanently consume the account creation identity url to prevent the
        # user from accidentally re-accessing the page after the process has
        # completed.  Also avoid malicious usage.
        id = s.pop(k)
        cherrypy.log.error('Consuming id {0}'.format(id), 'AccountController.create')

        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/account/create.html'.format(r.model['userSettings']['layout']))
        return template.render(
            model=r.model,
            oidIdentifier=id)
        
    @cherrypy.expose
    def submit(self, oidIdentifier, email):
        
        # See if the OpenID identifier or email are already in the database
        
        
        return 'submit {0} {1}'.format(oidIdentifier, email)