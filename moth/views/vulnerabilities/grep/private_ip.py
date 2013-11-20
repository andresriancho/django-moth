from moth.views.base.html_template_view import HTMLTemplateView


class PrivateIPDisclosureView(HTMLTemplateView):
    title = 'Private IP address exposure'
    description = 'Private IP address exposure'
    url_path = 'private_ip/private_ip.html'
    
    HTML = '''
    192.168.0.2
    '''

class PrivateIPDisclosureSlashView(HTMLTemplateView):
    title = 'Private IP address exposure (slash)'
    description = 'Private IP address exposure'
    url_path = 'private_ip/private_ip_2.html'
    
    HTML = '''
    \\10.1.2.3
    '''
    
class PrivateIPFalsePositiveOracleVersion(HTMLTemplateView):
    title = 'Oracle application server version false positive check'
    description = 'False positive check for Oracle server version'
    url_path = 'private_ip/false-positive-1.html'
    false_positive_check = True
    
    HTML = '''
    Server: Oracle-Application-Server-10g/10.1.2.0.2 Oracle-HTTP-Server
    '''

class PrivateIPFalsePositive2(HTMLTemplateView):
    title = 'Email address false positive check'
    description = 'Private IP address exposure false positive'
    url_path = 'private_ip/false-positive-2.html'
    false_positive_check = True
    
    HTML = '''
    abc@172.16.1.1
    '''
    
class PrivateIPFalsePositive3(HTMLTemplateView):
    title = 'Not IP address'
    description = 'Looks like an IP address, but not'
    url_path = 'private_ip/false-positive-3.html'
    false_positive_check = True
    
    HTML = '''
    10.10.10.10.10
    '''
    
class PrivateIPFalsePositive4(HTMLTemplateView):
    title = 'X-Forwarded-For header in body'
    description = 'X-Forwarded-For header in body false positive check'
    url_path = 'private_ip/false-positive-4.html'
    false_positive_check = True
    
    HTML = '''
    X-Forwarded-For: 192.168.1.1
    '''
