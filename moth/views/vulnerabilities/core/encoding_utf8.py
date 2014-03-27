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


class UTF8WithEncodedUCuteView(HTMLTemplateView):
    title = 'UTF-8 test with encoded u cute'
    description = 'UTF-8 test with u cute in filename (link is URL encoded)'
    url_path = u'vúlnerable.py'
    url_encode_path = True
    extra_headers = {'Content-Type': 'text/html; charset=utf-8'}

    HTML = HTML % {'charset': 'utf-8',
                   'body': u'Space filler'}


class UTF8WithEncodedRussianView(HTMLTemplateView):
    title = 'UTF-8 test with encoded Cyrillic cute'
    description = 'UTF-8 test with Cyrillic in filename (link is URL encoded)'
    url_path = u'проверка.py'
    url_encode_path = True
    extra_headers = {'Content-Type': 'text/html; charset=utf-8'}

    HTML = HTML % {'charset': 'utf-8',
                   'body': u'Space filler'}