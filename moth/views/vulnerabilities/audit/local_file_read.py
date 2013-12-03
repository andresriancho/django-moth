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
            os.path.exists(fname)
        except:
            context['html'] = 'Invalid file name.'
        else:
            if os.path.exists(fname):
                context['html'] = file(fname).read()
            else:
                context['html'] = 'Unknown file.'
            
        return render(request, self.template_name, context)
