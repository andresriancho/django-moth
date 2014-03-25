from moth.views.base.raw_path_view import RawPathTemplateView
from moth.views.base.html_template_view import HTMLTemplateView


class IAmHiddenView(RawPathTemplateView):
    title = 'A hidden file in the webroot'
    description = 'Simple unlinked file at /iamhidden.txt'
    url_path = 'iamhidden.txt'
    linked = False
    
    HTML = '''
    Please find me dir_bruter!
    '''


class HiddenDirectoryView(HTMLTemplateView):
    title = 'A hidden directory'
    description = 'Simple unlinked directory'
    url_path = 'spameggs/'
    linked = False

    HTML = '''
    I am a hidden directory!
    '''


class HiddenDirectoryView(HTMLTemplateView):
    title = 'A hidden directory inside the spameggs directory'
    description = 'Recursive test for directory inside directory'
    url_path = 'spameggs/foobar/'
    linked = False

    HTML = '''
    Double match! Found spameggs and then foobar inside it.
    '''

class HiddenFileView(HTMLTemplateView):
    title = 'A hidden file'
    description = 'Simple unlinked file inside the dir_bruter directory'
    url_path = 'hidden-inside-dir.txt'
    linked = False

    HTML = '''
    I am a hidden file!
    '''