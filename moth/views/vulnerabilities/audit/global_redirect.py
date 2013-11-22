from django.shortcuts import render
from django.shortcuts import render_to_response
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class GlobalRedirectFPCheckView(VulnerableTemplateView):
    description = title = 'False positive check for global redirect'
    url_path = 'global-redirect-fp.py?url=http://w3af.org/'
    false_positive_check = True
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['url']
        return render(request, self.template_name, context)
    
class GlobalRedirect302View(VulnerableTemplateView):
    description = title = '302 HTTP response code redirect'
    url_path = 'redirect-302.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'See HTTP response headers.'
        
        response = render_to_response(self.template_name, context)
        response.status_code = 302
        response['Location'] = request.GET['url']
        
        return response

class GlobalRedirect302FilteredView(VulnerableTemplateView):
    description = title = '302 HTTP response code redirect (filtered)'
    url_path = 'redirect-302-filtered.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        url = request.GET['url']
        
        if url.startswith('http://') or url.startswith('https://'): 
            context['html'] = 'Redirect not allowed.'
            response = render_to_response(self.template_name, context)
        else:
            context['html'] = 'See HTTP response headers.'
            response = render_to_response(self.template_name, context)
            response.status_code = 302
            response['Location'] = url 
        
        return response

class JavaScriptRedirectView(VulnerableTemplateView):
    description = title = 'JavaScript redirect'
    url_path = 'redirect-javascript.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        JS = '''<script language="javascript1.1">
                    <!--
                        window.location.replace("%s") ;
                    // -->
                </script>            
        '''
        
        context['html'] = JS % request.GET['url']
        return render(request, self.template_name, context)

class MetaTagRedirectView(VulnerableTemplateView):
    description = title = 'meta tag redirect'
    url_path = 'redirect-meta.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        msg = "You're being redirected in 3 seconds, please wait..."
        msg += '<META http-equiv="refresh" content="3;URL=%s">'
        
        context['html'] = msg % request.GET['url']
        return render(request, self.template_name, context)

class RedirectHeader302View(VulnerableTemplateView):
    description = title = '302 HTTP response code redirect with redirect header'
    url_path = 'redirect-header-302.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'See HTTP response headers.'
        
        response = render_to_response(self.template_name, context)
        response.status_code = 302
        response['Refresh'] = "0;url=%s" % request.GET['url']
        
        return response
