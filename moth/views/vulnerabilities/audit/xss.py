import re

from django.shortcuts import render
from django.shortcuts import render_to_response

from moth.forms.generic import TwoInputForm
from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.form_template_view import FormTemplateView


class SimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting'
    tags = ['trivial', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'simple_xss.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']
        return render(request, self.template_name, context)


class SimpleFormXSSView(FormTemplateView):
    title = 'Cross-Site scripting in form'
    tags = ['trivial', 'POST']
    description = 'Echo form parameter to HTML without any encoding'
    url_path = 'simple_xss_form.py'
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        context['message'] = request.POST['text']
        return render(request, self.template_name, context)


class FalsePositiveCheck499View(VulnerableTemplateView):
    title = '(almost) Cross-Site Scripting'
    tags = ['false-positive', 'GET', 'filtered']
    description = 'Echo query string parameter to HTML tag attribute removing'\
                  ' the single quotes which are present in the input.'
    url_path = '499_check.py?text=1'
    false_positive_check = True
    references = ['https://github.com/andresriancho/w3af/pull/499']
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        text = request.GET['text']
        text = text.replace('"', '')
        
        link = '<a href="http://external/abc/%s">Check link href</a>'
        
        context['html'] = link % text
        
        return render(request, self.template_name, context)


class XSSWithCSPView(VulnerableTemplateView):
    title = 'Cross-Site scripting with CSP enabled'
    tags = ['CSP', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'\
                  ' for new browsers CSP is enabled using response header.'
    url_path = 'xss_with_safe_csp.py?text=1'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']

        response = render_to_response(self.template_name, context)
        response['Content-Security-Policy'] = "default-src 'self'"

        return response


class XSSWithWeakCSPView(VulnerableTemplateView):
    title = 'Cross-Site scripting with weak CSP'
    tags = ['CSP', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'\
                  ' for new browsers CSP is enabled using response header.'\
                  ' The CSP policy is weak and does NOT protect the users.'
    url_path = 'xss_with_weak_csp.py?text=1'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']

        response = render_to_response(self.template_name, context)
        response['Content-Security-Policy'] = "script-src *;"

        return response


class BlacklistFilterXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting with trivial blacklist filter'
    tags = ['trivial', 'GET', 'blacklist']
    description = 'Echo query string parameter to HTML without any encoding'\
                  ' filter input by removing "script".'
    url_path = 'script_blacklist_xss.py?text=1'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text'].replace('script', '')
        return render(request, self.template_name, context)


class BlacklistFilterInsensitiveXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting with trivial blacklist filter'
    tags = ['trivial', 'GET', 'blacklist']
    description = 'Echo query string parameter to HTML without any encoding'\
                  ' filter input by removing "script", the replacement is done'\
                  ' in a case insensitive way.'
    url_path = 'script_insensitive_blacklist_xss.py?text=1'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        repl = re.compile('script', re.IGNORECASE)
        context['html'] = repl.sub('', request.GET['text'])
        return render(request, self.template_name, context)


class TwoInputFormXSSView(FormTemplateView):
    title = 'Cross-Site scripting in form with two inputs'
    tags = ['POST']
    description = 'Echo form parameter to HTML without any encoding only if'\
                  ' the other parameter was filled.'
    url_path = 'two_inputs_form.py'
    form_klass = TwoInputForm

    def post(self, request, *args, **kwds):
        context = self.get_context_data()

        if request.POST['name']:
            context['message'] = request.POST['address']
        else:
            context['message'] = 'Invalid name'

        return render(request, self.template_name, context)


class PersistentFormXSSView(FormTemplateView):
    title = 'Cross-Site scripting in form'
    tags = ['trivial', 'POST', 'persistent']
    description = 'Receives the data from an HTML form, stores it in session'\
                  ' and then displays it when issuing a GET without encoding.'
    url_path = 'persistent_xss_form.py'

    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        context['message'] = 'Data saved to DB.'

        request.session['header'] = request.POST['text']

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form = self.form_klass()

        context = self.get_context_data(form=form)

        header = request.session.get('header', '')
        context['header'] = header or 'No input data yet.'

        return render(request, self.template_name, context)