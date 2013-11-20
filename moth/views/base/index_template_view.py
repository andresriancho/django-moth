from django.views.generic import TemplateView
from django.shortcuts import render


class IndexTemplateView(TemplateView):
    '''
    When no URL pattern matches we generate a list with all the links in
    the subdirectory. We get here when the request is "foo/", there is no
    view with that pattern, and there are other views like "foo/abc" and
    "foo/def".
    '''
    # The template to use to render this view
    template_name = "moth/index-of.html"
    
    def __init__(self, url, subviews, *args, **kwds):
        '''
        :param url: The URL that lead to the generation of this index.
        :param subviews: The vulnerable views (which are inside this directory.
        '''
        self._url = url
        self._subviews = subviews
        super(IndexTemplateView, self).__init__(*args, **kwds)
    
    def _get_title(self):
        '''
        :return: Infer a title from the subview information.
        '''
        family, plugin = self._subviews[0].get_family_plugin()
        return plugin
    
    def get(self, request):
        '''
        :return: An HttpResponse with links to all subviews.
        '''
        links = [(v.title, v.url_path) for v in self._subviews]
        
        context = {}
        context['title'] = self._get_title()
        context['links'] = links
        
        return render(request, self.template_name, context)