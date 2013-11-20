from moth.views.base.html_template_view import HTMLTemplateView


class AppletObjectView(HTMLTemplateView):
    description = title = 'Applet object tag'
    url_path = 'applet.html'
    
    HTML = '''See HTML source code
    <applet src=""></applet>'''

class ObjectView(HTMLTemplateView):
    description = title = 'Object tag'
    url_path = 'object.html'
    
    HTML = '''See HTML source code
    <object src=""></object>'''
