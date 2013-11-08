import os
import string

from inspect import isclass
from datrie import Trie
from django.http import Http404

from moth.views.base.vulnerable_template_view import VulnerableTemplateView 


class RouterView(object):
    '''
    Route all HTTP requests to the corresponding view.
    '''
    
    DIR_EXCLUSIONS = set()
    FILE_EXCLUSIONS = set(['__init__.py',])
    
    def __init__(self):
        self._mapping = Trie(string.printable)
        self._view_files = []
        self._autoregister()
    
    def _autoregister(self):
        '''
        We go through the moth/views/ directory, importing all the modules
        and finding subclasses of VulnerableTemplateView. When we find one, we
        get the URL pattern from it, create an instance and call _register.
        
        :return: None, calls _register which stores the info in _mapping.
        '''
        for fname in self._get_vuln_view_files(self._get_vuln_view_directory()):
            for klass in self._get_views_from_file(fname):
                view_obj = klass()
                self._register(view_obj.url_path, view_obj)
    
    def _get_vuln_view_directory(self):
        '''
        :return: The directory we'll crawl to find the VulnerableTemplateView
                 subclasses. Vulnerable views are in "vulnerabilities". 
        '''
        root_path = os.path.realpath(os.path.curdir) + '/'
        self_path = os.path.dirname(os.path.realpath(__file__))
        rel_self_path = self_path.replace(root_path, '')
        return os.path.join(rel_self_path, 'vulnerabilities')
    
    def _get_vuln_view_files(self, directory):
        '''
        :param directory: Which directory to crawl
        :return: A list with all the files (with their path) in the
                 vulnerabilities directory.
        '''
        os.path.walk(directory, self._process_view_directory, None)
        return self._view_files
    
    def _process_view_directory(self, args, dirname, filenames):
        '''
        Called by os.path.walk to process each directory/filenames.
        
        :return: None, we save the views to self._view_files
        '''
        for excluded_path in self.DIR_EXCLUSIONS:
            if dirname.startswith(excluded_path):
                return
        
        for filename in filenames:
            if not filename.endswith('.py'):
                continue
            
            if filename in self.FILE_EXCLUSIONS:
                continue
            
            python_filename = os.path.join(dirname, filename)
            self._view_files.append(python_filename)
    
    def _get_views_from_file(self, fname):
        '''
        :param fname: The file name we need to import * from
        :return: A list of VulnerableTemplateView classes we find in the import 
        '''
        result = []
        
        mod_name = fname.replace('/', '.')
        mod_name = mod_name[:-len('.py')]
        module_inst = __import__(mod_name, fromlist=['*'])
        
        for var_name in dir(module_inst):
            var_inst = getattr(module_inst, var_name)
            if isclass(var_inst):
                if issubclass(var_inst, VulnerableTemplateView):
                    result.append(var_inst)
                
        return result
    
    def _generate_index(self, sub_views):
        '''
        When no URL pattern matches we generate a list with all the links in
        the subdirectory. We get here when the request is "foo/", there is no
        view with that pattern, and there are other views like "foo/abc" and
        "foo/def".
        
        :param sub_views: All the views which should be linked in the index page
        :return: An HttpResponse with the links to "foo/abc" and "foo/def".
        '''
        pass
    
    def _register(self, url_path, view_obj):
        '''
        Receives an url_path like '/abc/def/foo' and 'foo' and
        stores it in a Trie (https://pypi.python.org/pypi/datrie/).

        For now we don't support regular expression matching.
        
        :param url_path: An URL path like the one used in django's urls.py
        :param view_obj: The view object (not function)
        '''
        url_path = unicode(url_path)
        if url_path in self._mapping:
            raise RuntimeError('Duplicated URL: %s' % url_path)
        
        self._mapping[url_path] = view_obj
        
    def __call__(self, request, *args, **kwargs):
        '''
        This handles all requests. It should be short and sweet code.
        '''
        url_path = request.path[1:]
        
        if url_path in self._mapping:
            view_obj = self._mapping[url_path]
            return view_obj.dispatch(request, *args, **kwargs)
        
        else:
            # Try to create an "Index of" page
            sub_views = self._mapping.values(url_path)
            
            if sub_views:
                return self._generate_index(sub_views)
        
            # does not match
            raise Http404