from moth.views.base.html_template_view import HTMLTemplateView


class DirectoryIndexingView(HTMLTemplateView):
    title = 'Directory indexing'
    description = 'Directory indexing fingerprint test'
    url_path = 'index.html'
    
    HTML = '''<title>Index of /</title>'''
