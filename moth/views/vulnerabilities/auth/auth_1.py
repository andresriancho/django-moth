from django.shortcuts import render
from django.shortcuts import redirect

from moth.forms.generic import LoginForm
from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.form_template_view import FormTemplateView

VALID_USER = 'user@mail.com'
VALID_PASS = 'passw0rd'
REDIRECT = 'post_auth_xss.py?text=1'
TEST_ID = 'auth_1'
LOGIN_FORM = 'login_form.py'
LOGOUT = 'logout.py'
LOGIN_ID_KEY = 'logged_in_for'


class LoginSimpleView(FormTemplateView):
    title = 'Login for authentication trivial authentication test'
    tags = ['POST']
    description = 'A login form that redirects to a XSS on success.' \
                  ' Credentials: user@mail.com / passw0rd'
    url_path = LOGIN_FORM
    form_klass = LoginForm

    def post(self, request, *args, **kwds):
        context = self.get_context_data()

        if request.POST['username'] == VALID_USER and \
        request.POST['password'] == VALID_PASS:

            # Save the session so we know that this user has authenticated
            request.session[LOGIN_ID_KEY] = TEST_ID

            # Redirect to home
            return redirect(REDIRECT)

        context['header'] = 'Invalid credentials'
        context['form'] = self.form_klass()
        return render(request, self.template_name, context)


class PostAuthXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting vulnerability after login'
    tags = ['trivial', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = REDIRECT

    HTML_FMT = 'You may <a href="%s">logout</a> or read your input %s.'

    def get(self, request, *args, **kwds):
        if LOGIN_ID_KEY not in request.session:
            return redirect(LOGIN_FORM)

        if request.session[LOGIN_ID_KEY] != TEST_ID:
            return redirect(LOGIN_FORM)

        context = self.get_context_data()
        context['html'] = self.HTML_FMT % (LOGOUT, request.GET.get('text', '-'))
        return render(request, self.template_name, context)


class LogoutView(VulnerableTemplateView):
    title = 'Logout the current session'
    description = title
    url_path = LOGOUT

    def get(self, request, *args, **kwds):
        if LOGIN_ID_KEY not in request.session:
            return redirect(LOGIN_FORM)

        if request.session[LOGIN_ID_KEY] == TEST_ID:
            request.session[LOGIN_ID_KEY] = None

        return redirect(LOGIN_FORM)
