from moth.views.base.html_template_view import HTMLTemplateView


class DOMXssFalsePositiveView(HTMLTemplateView):
    title = 'DOM XSS false positive check'
    description = 'DOM XSS false positive check'
    url_path = 'dom-xss-fp.html?name=andres'
    false_positive_check = True
    
    HTML = '''
    Hi, welcome to our system
    
    <SCRIPT>
        var pos=document.URL.indexOf("name=")+5;
        foo(document.URL.substring(pos,document.URL.length));
    </SCRIPT>
    '''

class TrivialDOMXssView(HTMLTemplateView):
    title = 'DOM XSS trivial check'
    description = 'DOM XSS trivial check'
    url_path = 'dom-xss.html?name=andres'
    
    HTML = '''
    Hi
    
    <SCRIPT>
        var pos=document.URL.indexOf("name=")+5;
        document.write(document.URL.substring(pos,document.URL.length));
    </SCRIPT>

    , welcome to our system
    '''