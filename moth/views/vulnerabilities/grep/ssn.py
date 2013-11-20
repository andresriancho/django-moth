from moth.views.base.html_template_view import HTMLTemplateView


class SSNView(HTMLTemplateView):
    description = title = 'SSN exposure'
    url_path = 'with_ssn.html'
    
    HTML = '''
    <b>771</b>-<b>12</b>-<b>9876</b>
    '''

class FalsePositiveSSNView(HTMLTemplateView):
    description = title = 'SSN exposure (false positive)'
    url_path = 'without_ssn.html'
    false_positive_check = True
    
    HTML = '''
    <b>999</b>-<b>12</b>-<b>9876</b>
    '''
