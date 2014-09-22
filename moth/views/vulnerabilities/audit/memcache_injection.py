from django.contrib.auth.models import User
from django.shortcuts import render

from moth.forms.generic import GenericForm
from moth.views.base.form_template_view import FormTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView

import pylibmc
import cgi

class MemcacheInjectionView(VulnerableTemplateView):
    title = 'Batch injection'
    tags = ['memcache', 'memcached','injection' ]
    description = 'Trivial memcache batch injection in a set query'\
                  ' due to switched off by default sanity checks in'\
                  ' pylibmc. See issue #4406 for details.'
    url_path = 'memcache_value.py?key=1'


    def get(self, request, *args, **kwds):
        mc = pylibmc.Client(["127.0.0.1"])

        user_input = request.GET.get('key', '1')

        try:
            success = mc.set(str(user_input), 1)
            html = "The key was successfuly sent to cache!"
        except:
            html = "There was an error while calling set()"
            success = False


        context = self.get_context_data(html=html,
                                        success=success)

        return render(request, self.template_name, context)

class _MemcacheInjectionView(VulnerableTemplateView):
    title = 'Batch injection(internal test version)'
    tags = ['memcache', 'memcached','injection' ]
    description = 'THIS VERSION IS FOR INTERNAL TESTING PURPOSES!'\
                  'Trivial memcache batch injection in pylibmc. '\
                  ' It outputs the value of the key named "injected".'
    url_path = '_memcache_value.py?key=1'


    def get(self, request, *args, **kwds):
        mc = pylibmc.Client(["127.0.0.1"])

        user_input = request.GET.get('key', '1')

        success = mc.set(str(user_input), 1)


        mc = pylibmc.Client(["127.0.0.1"]) # making fresh connection instead of contaminated one

        injected = mc.get('injected')

        inj = str(injected)
        if not inj == '':
            inj = cgi.escape(inj, quote=True)
        html = "injected key: <b>"+inj+"</b>"
        context = self.get_context_data(html=html,
                                        success=True)

        return render(request, self.template_name, context)