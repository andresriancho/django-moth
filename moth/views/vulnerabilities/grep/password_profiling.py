from moth.views.base.html_template_view import HTMLTemplateView


class PasswordProfiling1View(HTMLTemplateView):
    title = 'Password profiling (page 1 of 2)'
    description = 'We just want to repeat some words so they make it to the'\
                  ' password profiling Top10.'
    url_path = 'index.html'
    
    HTML = '''
    <title>Password profiling</title>
    <h1 id="password">
        Password profiling
    </h1>
    <ol>
     <li>
        I just repeat Password here one more time, so it gets to the top
        of the list.
     </li>
    </ol>
    '''

class PasswordProfiling2View(HTMLTemplateView):
    title = 'Password profiling (page 2 of 2)'
    description = 'And we need to check that error pages are ignored.'
    url_path = 'error_page.html'
    
    HTML = '''<H1>Error page exception</H1>'''
