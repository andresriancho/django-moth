# -*- coding: utf-8 -*-

from moth.views.base.html_template_view import HTMLTemplateView


HTML = u'''<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=%(charset)s">
</head>
    <body>
        %(body)s
    </body>
</html>'''

#
#   FIXME: https://github.com/kmike/datrie/issues/20
#   FIXME: This issue blocks any progress with encoding testing
#

class UTF8WithJapaneseCharactersView(HTMLTemplateView):
    title = 'UTF-8 test with Japanese characters'
    description = 'UTF-8 test with Japanese characters in filename (link is' \
                  ' not URL encoded) and content.'
    url_path = u'改.py'
    extra_headers = {'Content-Type': 'text/html; charset=utf-8'}

    HTML = HTML % {'charset': 'utf-8',
                   'body': u'넓 넘 넙 넸 넹'.encode('utf-8')}


class UTF8WithECuteView(HTMLTemplateView):
    title = 'UTF-8 test with e cute'
    description = 'UTF-8 test with e cute in filename (link is not URL' \
                  ' encoded)'
    url_path = u'é.py'
    extra_headers = {'Content-Type': 'text/html; charset=utf-8'}

    HTML = HTML % {'charset': 'utf-8',
                   'body': u'Space filler'}