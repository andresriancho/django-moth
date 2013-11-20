from moth.views.base.html_template_view import HTMLTemplateView


class HTTPResponseInBodyView(HTMLTemplateView):
    description = title = 'HTTP response in HTTP response body'
    url_path = 'http_response.html'
    
    HTML = '''HTTP/1.0 200 OK'''

class HTTPRequestInBodyView(HTMLTemplateView):
    description = title = 'HTTP request in HTTP response body'
    url_path = 'http_request.html'
    
    HTML = '''GET /index.htm HTTP/1.1'''
