from moth.views.base.raw_path_view import RawPathTemplateView


class OraclePortal(RawPathTemplateView):
    title = 'Oracle portal'
    description = 'Oracle portal file'
    url_path = 'portal/page'
    linked = False

    HTML = '''
    <html><head><title>PPE is working</title></head><body>PPE version 1.3.4 is working.</body></html>
    '''

