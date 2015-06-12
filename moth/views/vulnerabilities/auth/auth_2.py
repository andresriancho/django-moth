from django.shortcuts import render
from django.shortcuts import redirect
from django.forms.widgets import TextInput, mark_safe
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from moth.views.vulnerabilities.auth.auth_1 import (LoginSimpleView,
                                                    REDIRECT, TEST_ID,
                                                    VALID_USER, VALID_PASS,
                                                    LOGIN_ID_KEY)

LOGIN_FORM = 'square_bracket_login_form.py'
LOGIN_USER_NAME = 'foo[user]'


class SquareBracketsInput(TextInput):
    """
    Hacking the django framework a little bit...
    """
    def render(self, name, value, attrs=None):
        return mark_safe('<input name="%s" />' % LOGIN_USER_NAME)


class SquareBracketLoginForm(forms.Form):
    username = forms.CharField(widget=SquareBracketsInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, * args, **kwargs):
        # pylint: disable=E1002
        super(SquareBracketLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-x'
        self.helper.field_class = 'col-lg-x'

        submit = Submit('Login', 'Login', css_class="btn-success")

        # generate layout
        self.helper.layout = Layout(Field('username'),
                                    Field('password'),
                                    submit)


class LoginSquareBracketView(LoginSimpleView):
    title = ('Login for authentication test containing square bracket in'
             'input name')
    tags = ['POST', 'bracket']
    description = 'A login form that redirects to a XSS on success.' \
                  ' Credentials: user@mail.com / passw0rd'
    url_path = LOGIN_FORM
    form_klass = SquareBracketLoginForm

    def post(self, request, *args, **kwds):
        context = self.get_context_data()

        if request.POST[LOGIN_USER_NAME] == VALID_USER and \
        request.POST['password'] == VALID_PASS:

            # Save the session so we know that this user has authenticated
            request.session[LOGIN_ID_KEY] = TEST_ID

            # Redirect to home
            return redirect(REDIRECT)

        context['header'] = 'Invalid credentials'
        context['form'] = self.form_klass()
        return render(request, self.template_name, context)
