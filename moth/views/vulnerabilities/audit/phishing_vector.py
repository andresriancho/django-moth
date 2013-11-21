from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class PhishingVectorIFrameView(VulnerableTemplateView):
    description = title = 'Iframe tag phishing vector (trivial)'
    url_path = 'iframe_phishing.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        tag = '<iframe id="datamain0" src="%s"></iframe>'
        context['html'] = tag % request.GET['url']
        return render(request, self.template_name, context)

class PhishingVectorFrameView(VulnerableTemplateView):
    description = title = 'Frame tag phishing vector (trivial)'
    url_path = 'frame_phishing.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        tag = '<frame src="%s"></iframe>'
        context['html'] = tag % request.GET['url']
        return render(request, self.template_name, context)

class PhishingVectorIFrameFilterView(VulnerableTemplateView):
    description = title = 'Iframe tag phishing vector with filter'
    url_path = 'http_blacklist_phishing.py?url=http://w3af.org/'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        tag = '<iframe src="%s"></iframe>'
        context['html'] = tag % request.GET['url'].replace('http://', '')
        return render(request, self.template_name, context)
