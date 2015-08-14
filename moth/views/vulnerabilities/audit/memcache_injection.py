import pylibmc
import cgi

from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class MemcacheInjectionView(VulnerableTemplateView):
    title = 'Batch injection'
    tags = ['memcache', 'memcached', 'injection']
    description = ('Trivial memcache batch injection in a set query'
                   ' due to switched off by default sanity checks in'
                   ' pylibmc. See w3af issue #4406 for details.')
    url_path = 'memcache_value.py?key=1'

    def get(self, request, *args, **kwds):
        mc = pylibmc.Client(['cache'])

        user_input = request.GET.get('key', '1')

        try:
            # pylint: disable=E1101
            success = mc.set(str(user_input), 1)
            # pylint: enable=E1101
            html = "The key was successfully sent to cache!"
        except:
            html = "There was an error while calling set()"
            success = False


        context = self.get_context_data(html=html,
                                        success=success)

        return render(request, self.template_name, context)


class _MemcacheInjectionView(VulnerableTemplateView):
    title = 'Batch injection (internal test version)'
    tags = ['memcache', 'memcached', 'injection']
    description = 'THIS VERSION IS FOR INTERNAL TESTING PURPOSES!'\
                  'Trivial memcache batch injection in pylibmc. '\
                  ' It outputs the value of the key named "injected".'
    url_path = '_memcache_value.py?key=1'
    linked = False

    def get(self, request, *args, **kwds):
        mc = pylibmc.Client(['cache'])

        user_input = request.GET.get('key', '1')

        try:
            # pylint: disable=E1101
            success = mc.set(str(user_input), 1)
            # pylint: enable=E1101
        except:
            html = "There was an error while calling set()"
            context = self.get_context_data(html=html,
                                            success=True)

            return render(request, self.template_name, context)

        # making fresh connection instead of contaminated one
        mc = pylibmc.Client(['cache'])

        # pylint: disable=E1101
        injected = mc.get('injected')
        # pylint: enable=E1101

        inj = str(injected)
        if not inj == '':
            inj = cgi.escape(inj, quote=True)
        html = "injected key: <b>"+inj+"</b>"
        context = self.get_context_data(html=html,
                                        success=True)

        return render(request, self.template_name, context)