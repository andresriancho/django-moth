from django.shortcuts import render

from moth.views.base.html_template_view import HTMLTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


EVENTVALIDATION = '/wEWAwLNx+2YBwKw59eKCgKcjoPABw=='
HTML = '''
<form name="aspnetForm" method="%(method)s" action="%(action)s" id="aspnetForm">
    <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUKMTEzMDczNTAxOWRk" />
    <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="%(eventvalidation)s" />

    <span>Search our news articles database</span>
    <input name="_ctl0:_ctl0:Content:Main:TextBox1" type="text" placeholder="Enter title (e.g. IBM)" id="_ctl0__ctl0_Content_Main_TextBox1" style="width:300px;" />
    <input type="submit" name="_ctl0:_ctl0:Content:Main:Button1" value="Query" id="_ctl0__ctl0_Content_Main_Button1" style="width:75px;" />
</form>
'''

class FormGetView(HTMLTemplateView):
    title = 'Form with special parameters and GET method'
    description = 'An HTML form with hidden field which has a "+" character'\
                  ' which is submitted using the GET method.'
    url_path = 'form_GET_spaces.html'
    
    HTML = HTML % {'method': 'GET',
                   'eventvalidation': EVENTVALIDATION,
                   'action': 'xss-get.py'}
    
class FormPOSTView(HTMLTemplateView):
    title = 'Form with special parameters and POST method'
    description = 'An HTML form with hidden field which has a "+" character'\
                  ' which is submitted using the POST method.'
    url_path = 'form_POST_spaces.html'
    
    HTML = HTML % {'method': 'POST',
                   'eventvalidation': EVENTVALIDATION,
                   'action': 'xss-post.py'}
    
def _handle(request, data_src, template_name, context):
    context['html'] = 'Invalid EVENTVALIDATION!'
    
    if '__EVENTVALIDATION' in data_src:
        if data_src['__EVENTVALIDATION'] == EVENTVALIDATION:
            context['html'] = data_src['_ctl0:_ctl0:Content:Main:TextBox1']
            
    return render(request, template_name, context)

class GETSimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting'
    tags = ['trivial', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'xss-get.py'
    
    def get(self, request, *args, **kwds):
        return _handle(request, request.GET, self.template_name,
                       self.get_context_data())

class POSTSimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting'
    tags = ['trivial', 'POST']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'xss-post.py'

    def get(self, request, *args, **kwds):
        return _handle(request, request.GET, self.template_name,
                       self.get_context_data())
        
    def post(self, request, *args, **kwds):
        return _handle(request, request.POST, self.template_name,
                       self.get_context_data())
    