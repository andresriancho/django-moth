import time

from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class DelayView(VulnerableTemplateView):
    description = title = 'Delay all responses 3 seconds'
    url_path = 'delay-responses.py?name=alice'

    def get(self, request, *args, **kwds):
        time.sleep(3)

        context = self.get_context_data()
        context['html'] = 'Delay success'

        return render(request, self.template_name, context)


