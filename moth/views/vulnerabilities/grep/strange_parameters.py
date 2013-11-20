from moth.views.base.html_template_view import HTMLTemplateView


class StrangeParametersView(HTMLTemplateView):
    title = 'Strange parameters'
    description = 'Links in the page contain strange parameters.'
    url_path = 'index.html'
    
    HTML = '''
    <a href="http://localhost/?b=method(a,c)">1</a>
    <a href="http://localhost/?c=x|y|z|d-3">2</a>
    '''

