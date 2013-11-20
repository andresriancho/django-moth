from django.views.generic import TemplateView
from django.shortcuts import render


class FamilyIndexTemplateView(TemplateView):
    '''
    When no URL pattern matches and it's a family URL (like /audit/ for example)
    we generate a page with links to all the tests in that directory.
    '''
    # The template to use to render this view
    template_name = "moth/index-of-family.html"
    
    def __init__(self, family, subviews, *args, **kwds):
        '''
        :param family: The URL that lead to the generation of this index.
        :param subviews: The vulnerable views (which are inside this directory.
        '''
        self._family = family
        self._subviews = subviews
        super(FamilyIndexTemplateView, self).__init__(*args, **kwds)
    
    def get(self, request):
        '''
        :return: An HttpResponse with links to all subviews.
        '''
        links = [(v.title, v.url_path) for v in self._subviews]
        
        context = {}
        context['family'] = self._family.title() 
        context['links'] = links
        
        return render(request, self.template_name, context)