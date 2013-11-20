from moth.views.base.html_template_view import HTMLTemplateView


class SHA1HashView(HTMLTemplateView):
    title = 'SHA1 hash found in body'
    description = 'SHA1 hash found on body, which needs analysis.'
    url_path = 'hash_find/sha1.html'
    
    HTML = '''
    e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e
    '''

class MD5HashView(HTMLTemplateView):
    title = 'MD5 hash found in body'
    description = 'MD5 hash found on body, which needs analysis.'
    url_path = 'hash_find/md5.html'
    
    HTML = '''
    b026324c6904b2a9cb4b88d6d61c81d1
    '''

class FalsePositiveHashView(HTMLTemplateView):
    title = 'No hash found in body'
    description = 'Make sure not all strings of a certain length are tagged'\
                  ' as hashes by our plugin.'
    url_path = 'hash_find/false-positive.html'
    false_positive_check = True
    
    HTML = '''
    11111111111111111111111111111111
    2222222222222222222aaaaaaaaaaaaa
    '''

