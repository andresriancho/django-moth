import re
import os

from django.http import Http404


class RouterView(object):
    '''
    Route all HTTP requests to the corresponding view.
    '''
    
    DIR_EXCLUSIONS = set()
    FILE_EXCLUSIONS = set(['__init__.py',])
    
    def __init__(self):
        self._mapping = {}
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
                self._register(view_obj.url, view_obj)
    
    def _get_vuln_view_directory(self):
        '''
        :return: The directory we'll crawl to find the VulnerableTemplateView
                 subclasses. Vulnerable views are in "vulnerabilities". 
        '''
        self_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(self_path, 'vulnerabilities')
    
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
        return []
    
    def _generate_index(self):
        '''
        When no URL pattern matches we generate a list with all the links in
        the subdirectory. We get here when the request is "foo/", there is no
        view with that pattern, and there are other views like "foo/abc" and
        "foo/def".
        
        :return: An HttpResponse with the links to "foo/abc" and "foo/def".
        '''
        pass
    
    def _register(self, url_pattern, view_obj):
        '''
        Receives an url_pattern like '/abc/def/foo' and stores that into
        the _mapping attribute. The way the example url_pattern is stored is:
        
        self._mapping = {
                         'abc': {
                                 'def':
                                       {
                                       re.compile('foo'): view_obj}
                                 }
                         }
        
        We store it like that in order to be able to easily generate "Index of"
        pages without reading the whole directory again.
        
        :param url_pattern: An URL pattern like the one used in django's urls.py
        :param view_obj: The view object (not function)
        '''
        splitted_pattern = self._split_url_pattern(url_pattern)
        
        # Now we store the pattern in our mapping dict
        current_dict = self._mapping
        for part in splitted_pattern[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            
            current_dict = current_dict[part]
            
        current_dict[splitted_pattern[-1]] = view_obj
        
    def _split_url_pattern(self, url_pattern):
        '''
        :param url_pattern: A string like '/abc/def/foo'
        :return: ['abc', 'def', re.compile('foo')] 
        '''
        if url_pattern.startswith('/'):
            url_pattern = url_pattern.path[1:]
            
        splitted_pattern = url_pattern.split('/')
        splitted_pattern[-1] = re.compile(splitted_pattern[-1])
        return splitted_pattern

    def __call__(self, request, *args, **kwargs):
        '''
        This handles all requests. It should be short and sweet code.
        '''
        splitted_pattern = self._split_url_pattern(request.path)
        
        for regex, view_obj in self._mapping.items():
            if regex.match(request.path[1:]):
                return view_obj.as_view()(request, *args, **kwargs)
        
        # does not match
        raise Http404