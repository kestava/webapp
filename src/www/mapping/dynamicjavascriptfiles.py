import cherrypy

class DynamicJavascriptFiles(object):

    @cherrypy.expose(alias='kestava.js')
    def kestava(self):
        cherrypy.response.headers['Content-Type'] = 'applications/javascript'
        
        return """
$(function() {{
    $('#userGreetingArea').click(kestava.userGreetingAreaClick);
}});

var kestava = (function() {{
    return {{
        'timelineServerHostname': '{timelineServerHostname}',
        'userGreetingAreaClick': function (ev) {{
            $('#userMenu').fadeToggle('fast');
        }}
    }};
}})();
""".format(timelineServerHostname=cherrypy.request.app.config['appSettings']['timelineServerHostname'])
