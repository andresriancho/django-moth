from moth.views.base.static_template_view import StaticFileView
from moth.views.base.html_template_view import HTMLTemplateView


class CreatedByOracleView(HTMLTemplateView):
    title = 'EICAR malware detection'
    description = 'I am not malware.'
    url_path = 'not-eicar'
    false_positive_check = True
    
    HTML = '''Not EICAR'''


class EICARCOM2View(StaticFileView):
    description = title = 'EICAR ClamAV zip test'
    STATIC_FILE = url_path = 'eicarcom2.zip'


class EICARCOMView(StaticFileView):
    description = title = 'EICAR ClamAV com test'
    STATIC_FILE = url_path = 'eicar.com'


class EICARTxtView(StaticFileView):
    description = title = 'EICAR ClamAV txt test'
    STATIC_FILE = url_path = 'eicar.com.txt'


class EICARZip2View(StaticFileView):
    description = title = 'EICAR ClamAV zip test'
    STATIC_FILE = url_path = 'eicar_com.zip'
