from django.shortcuts import render

from moth.views.base.html_template_view import HTMLTemplateView


class AzureHiddenView(HTMLTemplateView):
    title = 'Wordnet should find me!'
    description = 'A simple file that exists and should be found by wordnet'\
                  ' after understanding that filenames are colors (blue|green)'\
                  '.html'
    url_path = 'azure.html'
    linked = False
    
    HTML = '''
    Please find me wordnet!
    '''


class BlueView(HTMLTemplateView):
    title = 'Wordnet input data'
    tags = ['blue']
    description = 'A simple file to help wordnet understand that filenames are'\
                  ' colors.'
    url_path = 'blue.html'
    
    HTML = '''
    This is a blue page, we really like the blue color.
    '''


class RedView(HTMLTemplateView):
    title = 'Wordnet input data'
    tags = ['red']
    description = 'A simple file to help wordnet understand that filenames are'\
                  ' colors.'
    url_path = 'red.html'
    
    HTML = '''
    This is a red page, we really like the red color.
    '''


class GreenView(HTMLTemplateView):
    title = 'Wordnet should find me!'
    description = 'A simple file that exists and should be found by wordnet'\
                  ' after understanding that filenames are colors (blue|green)'\
                  '.html'
    url_path = 'green.html'
    linked = False
    
    HTML = '''
    Green is not linked, you shouldnt be here. Go home!
    '''


class HideView(HTMLTemplateView):
    title = 'Verb used as file name'
    description = 'Not linked, to be found by wordnet based on show.py'
    url_path = 'hide.py'
    linked = False
    
    HTML = '''
    I'm hidden and wordnet found me!
    '''


class ShowView(HTMLTemplateView):
    title = 'Wordnet test for file name and query string'
    description = 'Test verb in file name and word in query string'
    url_path = 'show.py?os=linux'
    
    def get(self, request, *args, **kwds):
        os = request.GET.get('os', 'linux')
        
        if os == 'linux':
            msg = 'We like linux very much, user friendly!'
        elif os == 'unix':
            msg = 'We LOVE unix (?)'
        elif os == 'windows':
            msg = 'Hating Windows, not easy to develop for that platform'
        else:
            msg = 'Invalid OS choice'
                
        context = self.get_context_data()
        context['html'] = msg
        return render(request, self.template_name, context)
