
import cherrypy

from modelobjectbase import ModelObjectBase
from model import grab_connection, get_row

class UserSettings(ModelObjectBase):
    
    key = 'userSettings'
    
    def read(self):
        o = {}
        
        # reasonable defaults
        o['layout'] = 'fixed'
        o['jQueryUiTheme'] = 'smoothness'
        
        i = cherrypy.session.get('user.account_id')
        if not i is None:
            with grab_connection('main') as conn:
                data = get_row(conn,
                    '''
                    select ui_layout, ui_theme from user_account_ui_settings
                    where ref_user_account_id = %(i)s
                    ''',
                    { 'i': i })
                
                if not data is None:
                    o['layout'] = data['ui_layout']
                    o['jQueryUiTheme'] = data['ui_theme']
        
        return o
        
    