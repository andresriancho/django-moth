# -*- coding: utf-8 -*-
import urllib

from django.http import Http404
from django.shortcuts import render

from moth.views.base.html_template_view import HTMLTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.vulnerabilities.core.encoding_utf8 import HTML


class RawJapaneseQueryStringView(VulnerableTemplateView):

    QUERY_STRING = u'頴英衛詠鋭液疫益'

    title = 'Link with a query string in Japanese'
    tags = ['not-encoded']
    description = 'Query string is unencoded and uses Japanese chars. Response'\
                  ' HTTP headers uses euc-jp.'
    url_path = u'raw-qs-jp.py?%s=1' % QUERY_STRING
    extra_headers = {'Content-Type': 'text/html; charset=euc-jp'}

    def get(self, request, *args, **kwds):
        if self.QUERY_STRING in request.GET:
            context = self.get_context_data()
            return render(request, self.template_name, context)
        else:
            raise Http404


class EncodedJapaneseQueryStringView(VulnerableTemplateView):

    QUERY_STRING = u'頴英衛詠鋭液疫益'

    title = 'Link with a query string in Japanese'
    tags = ['encoded']
    description = 'Query string is URL encoded and uses Japanese chars.'
    url_path = u'qs-jp.py?%s=1' % urllib.quote(QUERY_STRING.encode('utf-8'))
    extra_headers = {'Content-Type': 'text/html; charset=euc-jp'}

    def get(self, request, *args, **kwds):
        if self.QUERY_STRING in request.GET:
            context = self.get_context_data()
            return render(request, self.template_name, context)
        else:
            raise Http404