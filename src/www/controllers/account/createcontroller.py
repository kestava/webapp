
import cherrypy

from model import get_scalar_nc
from model.userdata import UserData
from model.usersettings import UserSettings
from model.sitedata import SiteData
from model.pagedata import PageData
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
    
    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData(),
        PageData()])
    @cherrypy.expose
    def submit(self, oidIdentifier, email):
        
        # See if the OpenID identifier or email are already in the database
        exists = get_scalar_nc(
            'main',
            """
            select exists (select 0 from unsilo.openid_accounts
            where openid_identifier = %(i)s) as a
            """,
            { 'i': oidIdentifier },
            'a')
        
        if exists:
            raise cherrypy.HTTPError(400, 'OpenID identifier in use.')
            
        #exists = get_scalar_nc(
        #    'main',
        #    """
        #    select exists (select 0 from unsilo.user_accounts
        #    where email like %(e)s) as a
        #    """,
        #    { 'e': email },
        #    'a')
        #
        #if exists:
        #    raise cherrypy.HTTPError(400, 'E-mail address in use.')
        #
        #return 'submit {0} {1}'.format(oidIdentifier, email)
        self._send_email(email)
        
        r = cherrypy.request
        r.model['pageData']['userEmail'] = email
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/account/create/submit.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        
    def _send_email(self, email):
        pass
        