from moth.views.base.html_template_view import HTMLTemplateView


class ValidMOTWView(HTMLTemplateView):
    title = 'Valid MOTW'
    description = 'Valid Mark of the Web'
    url_path = 'valid_MOTW.html'
    
    HTML = '''See HTML content for a valid MOTW
    <!-- saved from url=(0011)http://a/ -->'''

class InvalidMOTWView(HTMLTemplateView):
    title = 'Invalid MOTW'
    description = 'Invalid Mark of the Web'
    url_path = 'invalid_MOTW.html'
    
    HTML = '''See HTML source code for an invalid MOTW
    <!-- saved from      url='http://a/' -->'''
