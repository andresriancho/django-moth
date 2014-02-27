from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class SimpleEvalView(VulnerableTemplateView):
    title = 'Python eval() vulnerability'
    tags = ['trivial', 'GET']
    description = 'eval() the text query string without any validation and'\
                  ' output the result.'
    url_path = 'eval.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        try:
            result = eval(request.GET['text'])
        except SyntaxError:
            result = 'Invalid syntax'

        context['html'] = result
        return render(request, self.template_name, context)