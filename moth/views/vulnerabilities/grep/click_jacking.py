from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from django.shortcuts import render_to_response

X_FRAME_OPT = 'X-Frame-Options'


class ClickJackingVulnerableView(VulnerableTemplateView):
    title = 'ClickJacking X-Frame-Options'
    description = 'ClickJacking X-Frame-Options vulnerable'
    url_path = 'without_header.py'
    false_positive_check = True
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'No X-Frame-Options header'
        return render_to_response(self.template_name, context)


class ClickJackingNotVulnerableView(VulnerableTemplateView):
    title = 'ClickJacking X-Frame-Options'
    description = 'ClickJacking X-Frame-Options NOT vulnerable'
    url_path = 'with_header.py'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'View X-Frame-Options header'
        
        response = render_to_response(self.template_name, context)
        response[X_FRAME_OPT] = 'DENY'
        
        return response