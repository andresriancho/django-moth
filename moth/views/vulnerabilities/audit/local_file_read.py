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


class AppendExtensionLocalFileReadView(VulnerableTemplateView):
    description = title = 'Arbitrary local file read with extension appended'
    tags = ['GET']
    url_path = 'local_file_read_append_extension.py?file=section'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        fname = os.path.join(STATIC_DIR, request.GET['file']) + '.txt'

        try:
            context['html'] = file(fname).read()
        except:
            context['html'] = 'Error!'

        return render(request, self.template_name, context)


class FullPathFileReadView(VulnerableTemplateView):
    description = title = 'Full path arbitrary file read'
    tags = ['trivial', 'GET']
    url_path = 'local_file_read_full_path.py?file=section.txt'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        try:
            context['html'] = file(request.GET['file']).read()
        except:
            context['html'] = 'Error!'

        return render(request, self.template_name, context)


class EchoPasswdView(VulnerableTemplateView):
    description = title = 'Echo /etc/passwd file'
    tags = ['GET']
    url_path = 'false_positive_1.py?file=section.txt'
    false_positive_check = True

    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        html = request.GET['file']
        html += 'root:x:0:0:'
        context['html'] = html

        return render(request, self.template_name, context)