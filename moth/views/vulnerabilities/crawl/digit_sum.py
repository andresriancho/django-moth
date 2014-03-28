import random

from django.contrib.webdesign import lorem_ipsum
from django.http import Http404
from django.shortcuts import render

from moth.views.base.html_template_view import HTMLTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class FileSeedView(HTMLTemplateView):
    title = 'Seed file for digit-sum process'
    description = 'Just an initial file with numbers for digit-sum to work on.'
    url_path = 'index-3-1.html'

    HTML = '''
    Seed for the digit sum process.
    '''


class FileTargetView(HTMLTemplateView):
    title = 'Target file for digit-sum process'
    tags = ['not-linked']
    description = 'Target with numbers for digit-sum to identify.'
    url_path = 'index-2-1.html'
    linked = False

    HTML = '''
    Target for the digit sum process.
    '''


class QsDigitsView(VulnerableTemplateView):
    title = 'Digit sum query string'
    tags = ['query-string', 'GET']
    description = 'Test file for digit sum. Content differs when changing ids.'\
                  ' Valid ids are 20, 21, 22 and 23.'
    url_path = 'index1.py?id=20'

    VALID_IDS = [20, 21, 22, 23]

    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        _id = request.GET['id']

        if _id.isdigit() and int(_id) in self.VALID_IDS:
            parag = int((int(_id) - 20) * 4)

            # A bad thing about the lorem_ipsum module is that it will generate
            # RANDOM texts each time we call it, that means that in some cases
            # the plugin will detect big changes, and in some others it won't.
            #
            # To be able to fix this issue, we set the random seed
            #
            # Keep in mind that with some seeds the test will PASS, and with
            # many others it won't. Lucky me, it passed on the second try.
            random.seed(1)

            context['html'] = '<br><br>'.join(lorem_ipsum.paragraphs(parag))
        else:
            raise Http404

        return render(request, self.template_name, context)

