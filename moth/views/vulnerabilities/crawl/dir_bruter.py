from moth.views.base.raw_path_view import RawPathTemplateView


class IAmHiddenView(RawPathTemplateView):
    title = 'A hidden file'
    description = 'Simple unlinked file at /iamhidden.txt'
    url_path = 'iamhidden.txt'
    linked = False
    
    HTML = '''
    Please find me dir_bruter!
    '''