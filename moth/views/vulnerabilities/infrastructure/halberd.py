import random
import datetime

from django.shortcuts import render_to_response

from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class RandomHeaderView(VulnerableTemplateView):
    title = 'Randomly adds an HTTP header'
    tags = ['GET', 'HTTP header']
    description = 'One out of three requests will have an HTTP header. This'\
                  ' should be enough to convince Halberd that something is'\
                  ' going on.'
    url_path = 'halberd.py'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'See HTTP response headers.'
        response = render_to_response(self.template_name, context)
        response.status_code = 200

        # Date: Wed, 26 Feb 2014 17:56:30 GMT
        date_fmt = "%a, %d %b %Y %H:%M:%S GMT"
        now = datetime.datetime.now()

        if random.randint(0, 2) == 0:
            time_in_header = now
        else:
            time_in_header = now + datetime.timedelta(seconds=120)

        response['Date'] = time_in_header.strftime(date_fmt)

        return response