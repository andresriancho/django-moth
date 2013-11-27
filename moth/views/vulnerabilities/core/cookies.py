from django.shortcuts import render
from django.shortcuts import render_to_response
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


COOKIE_NAME = 'TestCookie'
COOKIE_VALUE = 'something from somewhere'


class SetCookieView(VulnerableTemplateView):
    description = title = 'Sets a TestCookie for testing'
    url_path = 'set-cookie.py'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'See HTTP response headers.'
        
        response = render_to_response(self.template_name, context)
        response['Set-Cookie'] = '%s=%s;' % (COOKIE_NAME, COOKIE_VALUE)
        
        return response

class GetCookieView(VulnerableTemplateView):
    description = title = 'Checks for TestCookie'
    url_path = 'get-cookie.py'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        if COOKIE_NAME in request.COOKIES:
            if request.COOKIES[COOKIE_NAME]:
                msg = 'Cookie was sent.'
        else:
            msg = 'Cookie was NOT sent.'
        
        context['html'] = msg
        
        return render(request, self.template_name, context)

