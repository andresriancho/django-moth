from moth.views.base.html_template_view import HTMLTemplateView


class CodeDisclosureView(HTMLTemplateView):
    description = title = 'Code disclosure'
    url_path = 'code_disclosure.html'
    
    HTML = '''
    View HTML source code
    <?
    read my code!
    ?>
    '''

class FalsePositiveCodeDisclosureView(HTMLTemplateView):
    description = title = 'Code disclosure (false positive)'
    url_path = 'no_code_disclosure.html'
    false_positive_check = True
    
    HTML = '''
    read my code!
    ?>
    '''
