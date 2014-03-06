import os
import string

from inspect import isclass
from datrie import Trie
from django.http import Http404

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.index_template_view import IndexTemplateView
from moth.views.base.family_index_template_view import FamilyIndexTemplateView
from moth.views.base.html_template_view import HTMLTemplateView
from moth.views.base.static_template_view import StaticFileView
from moth.views.base.form_template_view import FormTemplateView

from moth.utils.plugin_families import get_plugin_families


class RouterView(object):
    '''
    Route all HTTP requests to the corresponding view.
    '''
    
    KLASS_EXCLUSIONS = {HTMLTemplateView, VulnerableTemplateView,
                        StaticFileView, FormTemplateView}
    DIR_EXCLUSIONS = set()
    FILE_EXCLUSIONS = {'__init__.py'}
    
    def __init__(self):
        self._plugin_families = set(get_plugin_families())
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
                try:
                    view_obj = klass()
                    self._register(view_obj.get_url_path(), view_obj)
                except Exception, e:
                    msg = 'An exception occured while trying to register %s: "%s"'
                    raise RuntimeError(msg % (view_obj, e))
    
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
                if issubclass(var_inst, VulnerableTemplateView) and \
                var_inst not in self.KLASS_EXCLUSIONS:
                    result.append(var_inst)
                
        return result
    
    def _generate_index(self, request, url_path, sub_views):
        '''
        When no URL pattern matches we generate a list with all the links in
        the subdirectory. We get here when the request is "foo/", there is no
        view with that pattern, and there are other views like "foo/abc" and
        "foo/def".
        
        :param sub_views: All the views which should be linked in the index page
        :return: An HttpResponse with the links to "foo/abc" and "foo/def".
        '''
        index = IndexTemplateView(url_path, sub_views)
        return index.get(request)
    
    def _generate_family_index(self, request, family, sub_views):
        index = FamilyIndexTemplateView(family, sub_views)
        return index.get(request)
    
    def _register(self, url_path, view_obj):
        '''
        Receives an url_path like '/abc/def/foo' and 'foo' and
        stores it in a Trie (https://pypi.python.org/pypi/datrie/).

        For now we don't support regular expression matching.
        
        :param url_path: An URL path like the one used in django's urls.py
        :param view_obj: The view object (not function)
        '''
        family, plugin = view_obj.get_family_plugin()
        
        url_path = unicode('%s/%s/%s' % (family, plugin, url_path))
        if url_path in self._mapping:
            msg = 'Duplicated URL "%s" from "%s".'
            raise RuntimeError(msg % (url_path, view_obj))
        
        self._mapping[url_path] = view_obj
        
    def _extract_family_from_path(self, url_path):
        '''
        :return: The family name from the url_path. For example:
                    - /audit/ returns 'audit'
                    - /grep/foo/bar returns 'grep'
                
        :raises ValueError: When the path does not contain a family name as
                            first directory.
        '''
        path_family = url_path.split('/')[0]
        if path_family in self._plugin_families:
            return path_family
        
        raise ValueError('Unknown family "%s"' % path_family)
    
    def _is_plugin_family_request(self, url_path):
        '''
        :return: True when the url_path is just for the family, for example:
                     - /audit/
                     - /grep/
                     
                 Will return false for:
                     - /audit/xss/
                     - /grep/empty/index.html
        '''
        for known_family in self._plugin_families:
            if ('%s/' % known_family) == url_path:
                return True
            
        return False
    
    def __call__(self, request, *args, **kwargs):
        '''
        This handles all requests. It should be short and sweet code.
        '''
        url_path = request.path[1:]
        
        if url_path in self._mapping:
            view_obj = self._mapping[url_path]
            return view_obj.dispatch(request, *args, **kwargs)
        
        elif self._is_plugin_family_request(url_path):
            # Try to create an "Index of" page for this family (grep, audit, etc.)
            sub_views = self._mapping.values(url_path)
            family = self._extract_family_from_path(url_path)
            
            if sub_views:
                return self._generate_family_index(request, family, sub_views)
        
        else:
            # Try to create an "Index of" page for vulnerabilities
            sub_views = self._mapping.values(url_path)
            
            if sub_views:
                return self._generate_index(request, url_path, sub_views)
        
        # does not match anything we know about
        raise Http404