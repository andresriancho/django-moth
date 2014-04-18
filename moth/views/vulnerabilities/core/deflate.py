import zlib

from django.template.loader import render_to_string
from django.http import HttpResponse

from moth.views.base.html_template_view import HTMLTemplateView


class DeflateEncodingView(HTMLTemplateView):
    description = title = 'This view uses deflate/zlib to encode the response'
    url_path = 'deflate.html'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'View HTTP response headers.'
        response_body = render_to_string(self.template_name, context)

        compressed_body = zlib.compress(response_body)

        response = HttpResponse(compressed_body)
        response['Content-Encoding'] = 'deflate'
        response['Content-Length'] = len(compressed_body)
        return response
