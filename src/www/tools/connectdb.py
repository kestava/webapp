import cherrypy

from model.database import make_connection, close_connection

class ConnectDb(cherrypy.Tool):
    
    def __init__(self):
        super(ConnectDb, self).__init__('before_request_body', self.__connect)
        
    def __connect(self):
        make_connection()

class DisconnectDb(cherrypy.Tool):
    
    def __init__(self):
        super(DisconnectDb, self).__init__('on_end_request', self.__disconnect)

    def __disconnect(self):
        if hasattr(cherrypy.request, 'db'):
            close_connection()
                        
cherrypy.tools.connect_db = ConnectDb()
cherrypy.tools.disconnect_db = DisconnectDb()