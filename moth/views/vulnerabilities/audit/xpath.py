import os
import cgi

# pylint: disable=E0611
from lxml import etree
from lxml.etree import XPathEvalError, ParserError, XMLParser
# pylint: enable=E0611

from django.shortcuts import render

from moth.views.base.static_template_view import STATIC_DIR
from moth.views.base.form_template_view import FormTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView

XML_DB = os.path.join(STATIC_DIR, 'xpath.xml')


class SingleQuoteXpathView(FormTemplateView):
    title = 'XPath injection in single quoted string'
    tags = ['POST', 'single-quote']
    description = 'Concatenate the user input with a pre-defined xpath query' \
                  ' with single quoted string and send it to lxml'
    url_path = 'xpath-attr-single.py'
    xpath_query_fmt = "/articles/article[@id='%s']/title"

    def post(self, request, *args, **kwds):
        context = self.get_context_data()

        user_input = request.POST['text']
        user_input = user_input.replace(' ', '-')
        if user_input:
            context['message'] = run_xpath(self.xpath_query_fmt % user_input)
        else:
            context['message'] = 'Please enter your query.'

        return render(request, self.template_name, context)


class DoubleQuoteXpathView(SingleQuoteXpathView):
    title = 'XPath injection in double quoted string'
    tags = ['POST', 'double-quote']
    description = 'Concatenate the user input with a pre-defined xpath query' \
                  ' with double quoted string and send it to lxml'
    url_path = 'xpath-attr-double.py'
    xpath_query_fmt = '/articles/article[@id="%s"]/title'


class OrQueryXpathView(SingleQuoteXpathView):
    title = 'XPath injection in OR query'
    tags = ['POST', 'or']
    description = 'Concatenate the user input with a pre-defined xpath query' \
                  ' with OR operator and send it to lxml'
    url_path = 'xpath-attr-or.py'
    xpath_query_fmt = "/articles/article/tags[tag='php' or tag='%s']/../title"


class TagQueryXpathView(SingleQuoteXpathView):
    title = 'XPath injection in tag section of query'
    tags = ['POST', 'tag']
    description = 'Concatenate the user input with a pre-defined xpath query' \
                  ' tag section and send it to lxml'
    url_path = 'xpath-attr-tag.py'
    xpath_query_fmt = "/articles/article/%s"


class FalsePositiveCheckXPathDetectionXSS(VulnerableTemplateView):
    title = 'XPath false positive check'
    tags = ['trivial', 'GET', 'xss']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'false_positive_echo.py?text=1'
    false_positive_check = True

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']
        return render(request, self.template_name, context)


class FalsePositiveCheckXPathDetectionStatic(VulnerableTemplateView):
    title = 'XPath false positive check'
    tags = ['trivial', 'GET', 'empty']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'false_positive_static.py?text=1'
    false_positive_check = True

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'Static content.'
        return render(request, self.template_name, context)


def run_xpath(query):
    """
    Run a query against the XML_DB and return a string with the results.
    """
    # Make a good HTML tree
    try:
        parser = XMLParser()
        # pylint: disable=E1101
        dom = etree.fromstring(file(XML_DB).read(), parser)
        # pylint: enable=E1101
    except ParserError, e:
        return 'Unable to parse document: %s' % e

    # Run the xpath, and return the results
    try:
        nodes = dom.xpath(query)
    except XPathEvalError, e:
        return 'Invalid XPath Expression: %s' % e

    if type(nodes) == bool:
        return 'Your query returned a boolean: %s' % nodes
    else:
        node_strings = []

        for node in nodes:
            try:
                # pylint: disable=E1101
                s = etree.tostring(node,
                                   encoding='unicode',
                                   pretty_print=True).strip()
                node_strings.append(cgi.escape(s))
                # pylint: enable=E1101
            except TypeError:
                # Returned a text node, not an element.
                if len(node.strip()) > 0:
                    node_strings.append(node)

        if node_strings:
            return '<br>'.join(node_strings)
        else:
            return 'Empty search result'