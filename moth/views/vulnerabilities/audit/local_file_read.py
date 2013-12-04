import os

from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.static_template_view import STATIC_DIR


class TrivialLocalFileReadView(VulnerableTemplateView):
    description = title = 'Arbitrary local file read'
    tags = ['trivial', 'GET']
    url_path = 'local_file_read.py?file=section.txt'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        fname = os.path.join(STATIC_DIR, request.GET['file'])

        try:
            context['html'] = file(fname).read()
        except:
            context['html'] = 'Error!'
            
        return render(request, self.template_name, context)
