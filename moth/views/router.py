import re

from django.http import Http404, HttpResponse
from django.utils.datastructures import SortedDict


class RouterView(object):
    def __init__(self):
        self._mapping = SortedDict()
        self._autoregister()
    
    def _autoregister(self):
        '''
        We go through the moth/views/ directory, importing all the modules
        and finding subclasses of VulnerableTemplateView. When we find one, we
        get the URL pattern from it, create an instance and call _register.
        
        :return: None, calls _register which stores the info in _mapping.
        '''
        pass
    
    def _generate_list(self):
        '''
        When no URL pattern matches we generate a list with all the links in
        the subdirectory. We get here when the request is "foo/", there is no
        view with that pattern, and there are other views like "foo/abc" and
        "foo/def".
        
        :return: An HttpResponse with the links to "foo/abc" and "foo/def".
        '''
        pass
    
    def _register(self, regex, view_func):
        self.mapping[re.compile(regex)] = view_func

    def __call__(self, request, *args, **kwargs):
        '''
        This handles all requests. It should be short and sweet code.
        '''
        for regex, view_func in self._mapping.items():
            if regex.match(request.path[1:]):
                return view_func(request, *args, **kwargs)
        
        # does not match
        raise Http404