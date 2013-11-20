from moth.views.base.html_template_view import HTMLTemplateView


class WSDLSignatureView(HTMLTemplateView):
    title = 'WSDL file signature'
    description = 'WSDL file signature with xs:int'
    url_path = 'wsdl.html'
    
    HTML = '''xs:int'''
