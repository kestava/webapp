
import cherrypy

from views import create_view
from controllers.accountsettingscontroller import AccountSettingsController

class AccountPages(object):

    @cherrypy.expose
    def index(self):
        return 'Your Public Profile'

    @cherrypy.tools.connect_db()
    @cherrypy.expose
    def settings(self):
        c = AccountSettingsController()
        return create_view(c)