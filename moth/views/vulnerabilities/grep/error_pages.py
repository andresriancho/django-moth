from moth.views.base.html_template_view import HTMLTemplateView


class ApacheErrorPageView(HTMLTemplateView):
    title = 'Apache error page'
    description = 'Apache error page signature'
    url_path = 'index.html'
    
    HTML = '''<H1>Error page exception</H1>'''
