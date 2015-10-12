import re
import json
import requests

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from moth.forms.generic import LoginForm
from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.form_template_view import FormTemplateView

VALID_USER = 'user@mail.com'
VALID_PASS = 'passw0rd'
REDIRECT = 'launchpad.py'
JSON_QUERY = 'json-query-balance.py'
GET_QUERY = 'query-balance.py'
TEST_ID = 'ssrf_1'
LOGIN_FORM = 'login_form.py'
LOGOUT = 'logout.py'
LOGIN_ID_KEY = 'logged_in_for_ssrf'
USER_ID = 'user_id'


class LoginSimpleView(FormTemplateView):
    title = 'Authenticated SSRF test'
    tags = ['POST', 'SSRF']
    description = ('Authenticated SSRF test.'
                   ' Credentials: user@mail.com / passw0rd')
    url_path = LOGIN_FORM
    form_klass = LoginForm

    def post(self, request, *args, **kwds):
        context = self.get_context_data()

        if (request.POST['username'] == VALID_USER and
            request.POST['password'] == VALID_PASS):

            # Save the session so we know that this user has authenticated
            request.session[LOGIN_ID_KEY] = TEST_ID
            request.session[USER_ID] = 1

            # Redirect to home
            return redirect(REDIRECT)

        context['header'] = 'Invalid credentials'
        context['form'] = self.form_klass()
        return render(request, self.template_name, context)


class SSRFLaunchpadView(VulnerableTemplateView):
    title = 'SSRF launchpad'
    tags = ['trivial', 'GET']
    description = 'Access user balance'
    url_path = REDIRECT

    HTML_FMT = ('<a href="%s?filter=all">Refresh balance</a><br>'
                '<a href="%s">Logout</a><br>')

    def get(self, request, *args, **kwds):
        if LOGIN_ID_KEY not in request.session:
            return redirect(LOGIN_FORM)

        if request.session[LOGIN_ID_KEY] != TEST_ID:
            return redirect(LOGIN_FORM)

        context = self.get_context_data()
        context['html'] = self.HTML_FMT % (GET_QUERY, LOGOUT)
        return render(request, self.template_name, context)


class GetSSRF(VulnerableTemplateView):
    title = 'Query balance on backend API based on query string'
    linked = False
    url_path = GET_QUERY

    def validate_url(self, url):
        for encoded in re.findall('%(.*){0,2}', url):
            if not encoded:
                raise Exception('Invalid URL')

            for i in encoded:
                if i not in 'abcdef0123456789':
                    raise Exception('Invalid URL')

        return True

    def get(self, request, *args, **kwds):
        if LOGIN_ID_KEY not in request.session:
            return redirect(LOGIN_FORM)

        if request.session[LOGIN_ID_KEY] != TEST_ID:
            return redirect(LOGIN_FORM)

        data_filter = request.GET.get('filter', 'all')
        user = request.session[USER_ID]
        args = (JSON_QUERY, data_filter, user)
        url = 'http://localhost:8000/audit/ssrf/%s?filter=%s&user=%s' % args

        try:
            self.validate_url(url)
            response_json = requests.get(url).json()
        except Exception, e:
            html = ('An error occurred while requesting "%s", the'
                    ' exception message was: "%s"')
            html %= (url, e)
        else:
            try:
                html = 'Your balance is: %s' % response_json['balance']
            except KeyError:
                html = 'Error! %s' % response_json['error']

        context = self.get_context_data()
        context['html'] = html
        return render(request, self.template_name, context)


class JsonSSRF(VulnerableTemplateView):
    url_path = JSON_QUERY
    linked = False
    title = 'JSON query balance'
    BALANCE_DATA = {1: {'all': 390, 'last-month': 15, 'last-year': 200},
                    2: {'all': 8650, 'last-month': 998, 'last-year': 21200}}

    def get(self, request, *args, **kwds):
        remote_addr = request.META.get('REMOTE_ADDR', None)
        if remote_addr is None or remote_addr != '127.0.0.1':
            data = {'error': 'Unknown source'}
            return self.build_response(data)

        user = request.GET.get('user', None)

        if user is None:
            data = {'error': 'No user specified'}
            return self.build_response(data)

        # Get the first from the list, this is required for SSRF
        user = request.GET.getlist('user')[0].strip()
        
        if not user.isdigit():
            data = {'error': 'Invalid user'}
            return self.build_response(data)

        user = int(user)
        if user not in self.BALANCE_DATA:
            data = {'error': 'Unknown user'}
            return self.build_response(data)

        data_filter = request.GET.get('filter', None)
        if data_filter is None:
            data = {'error': 'No filter specified'}
            return self.build_response(data)

        if data_filter not in self.BALANCE_DATA[1].keys():
            data = {'error': 'Invalid filter'}
            return self.build_response(data)

        data = {'balance': self.BALANCE_DATA[user][data_filter]}
        return self.build_response(data)

    def build_response(self, data):
        return HttpResponse(json.dumps(data), content_type='application/json')


class LogoutView(VulnerableTemplateView):
    title = 'Logout the current session'
    description = title
    url_path = LOGOUT

    def get(self, request, *args, **kwds):
        if LOGIN_ID_KEY not in request.session:
            return redirect(LOGIN_FORM)

        if request.session[LOGIN_ID_KEY] == TEST_ID:
            request.session[LOGIN_ID_KEY] = None
            request.session[USER_ID] = None

        return redirect(LOGIN_FORM)
