
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pformat, pprint

import cherrypy

from model import get_scalar_nc

from model.viewdata.userdata import UserData
from model.viewdata.usersettings import UserSettings
from model.viewdata.sitedata import SiteData
from model.viewdata.pagedata import PageData

from model.uniquerequest import UniqueRequest
from model.useraccount import UserAccount

from lib.sessionhelper import SessionHelper
from lib import make_netloc

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
        
        s = SessionHelper()
        
        # See if the OpenID identifier or email are already in the database
        exists = get_scalar_nc(
            'main',
            """
            select exists (select 0 from openid_accounts
            where openid_identifier = %(i)s) as a
            """,
            { 'i': oidIdentifier },
            'a')
        
        if exists:
            raise cherrypy.HTTPError(400, 'OpenID identifier in use.')
            
        exists = get_scalar_nc(
            'main',
            """
            select exists (select 0 from user_accounts
            where email like %(e)s) as a
            """,
            { 'e': email },
            'a')
        
        message = self._email_exists_message(email, oidIdentifier) \
            if exists \
            else self._new_account_message(email, oidIdentifier)
        
        self._send_email(
            message=message,
            smtpServer=self._get_smtp_server(),
            email=email)
        
        r = cherrypy.request
        r.model['pageData']['userEmail'] = email
        env = r.app.jinjaEnv
        template = env.get_template(
            'html/{0}/account/create/submit.html'.format(
                r.model['userSettings']['layout']))
        return template.render(model=r.model)
        
    def _email_exists_message(self, email, oidIdentifier):
        print('Inside _email_exists_message')
        c = cherrypy.request.app.config
        env = cherrypy.request.app.jinjaEnv
        s = SessionHelper()
        u = UniqueRequest()
        
        value = u.create(
            sessionKey=cherrypy.session.id,
            requestKey='add_openid.existing_account',
            data='|'.join([str(UserAccount().id_from_email(email)), oidIdentifier]))
        s.push('add_openid.existing_account', value)
            
        # need to pass the session id in case they visit it using a different browser
        linkAddress = 'http://{0}/account/add/email?sessionKey={1}&request={2}'.format(
            make_netloc(),
            cherrypy.session.id,
            s.peek('add_openid.existing_account'))
        
        text = env.get_template('email/account/create/existing/verify.txt').render(
            siteName=c['appSettings']['siteName'],
            email=email,
            identityURL=oidIdentifier,
            linkAddress=linkAddress)
        html = env.get_template('email/account/create/existing/verify.html').render(
            siteName=c['appSettings']['siteName'],
            email=email,
            identityURL=oidIdentifier,
            linkAddress=linkAddress)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Confirm Add E-mail Address'
        msg['From'] = self._get_from_address()
        msg['To'] = email
        
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        return msg
    
    def _new_account_message(self, email, oidIdentifier):
        print('Inside _new_account_message')
        raise NotImplementedError()
        
    def _send_email(self, message, smtpServer, email):
        s = smtplib.SMTP(host=smtpServer)
        try:
            s.sendmail(
                from_addr=self._get_from_address(),
                to_addrs=[email],
                msg=message.as_string())
        finally:
            s.quit()
        
    def _get_from_address(self):
        return 'accounts@{0}'.format(cherrypy.request.app.config['appSettings']['siteHostname'])
        
    def _get_smtp_server(self):
        return cherrypy.request.app.config['appSettings']['email.smtp_server']