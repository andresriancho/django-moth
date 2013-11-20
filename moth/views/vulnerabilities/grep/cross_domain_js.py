from moth.views.base.html_template_view import HTMLTemplateView


class CrossDomainMixed(HTMLTemplateView):
    title = 'Cross Domain JavaScript (mixed)'
    description = 'Mixed javascript, same domain and external.'
    url_path = 'cross_domain_script_mixed.html'
    
    HTML = '''
    <html>
            <script src="http://moth/foo.js"></script>
            <script src="http://www.w3af.org/foo.js"></script>
            <script src="/foo.js"></script>
    </html>
    '''

class CrossDomainLocal(HTMLTemplateView):
    title = 'Cross Domain JavaScript (same domain)'
    description = 'Javascript from the same domain'
    url_path = 'local_script.html'
    false_positive_check = True
    
    HTML = '''
    <html>
        <script src="/foo.js"></script>
    </html>
    '''

class CrossDomainExternal(HTMLTemplateView):
    title = 'Cross Domain JavaScript (external)'
    description = 'Javascript from an external domain'
    url_path = 'cross_domain_script.html'
    
    HTML = '''
    <html>
            <script src="http://www.w3af.org/foo.js"></script>
    </html>
    '''

class CrossDomainWithType(HTMLTemplateView):
    title = 'Cross Domain JavaScript (type attr)'
    description = 'Javascript from an external domain with type attr'
    url_path = 'cross_domain_script_with_type.html'
    
    HTML = '''
    <html>
            <script type="text/javascript" SRC="http://www.w3af.org/foo.js"></script>
    </html>
    '''
