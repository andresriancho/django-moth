from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class Error500View(VulnerableTemplateView):
    title = 'Error 500 detection'
    description = 'Returns an error 500 when the id parameter value is not 1.'
    url_path = '500.py?id=1'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        if request.GET['id'] == '1':
            status = 200 
            context['html'] = 'Ok! HTTP response code is 200.'
        else:
            status = 500
            context['html'] = 'Error! HTTP response code is 500.'

        return render(request, self.template_name, context, status=status)
