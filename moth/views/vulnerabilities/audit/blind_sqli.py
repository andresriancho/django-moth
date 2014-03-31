from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.vulnerabilities.audit.sql_injection import get_users
from moth.views.base.form_template_view import FormTemplateView
from moth.forms.generic import GenericForm


class BlindSQLIntegerFormView(FormTemplateView):
    template_name = "moth/vulnerability-users-table.html"
    title = 'Trivial blind SQL injection in form'
    tags = ['WHERE', 'integer', 'form', 'blind']
    description = 'Trivial blind SQL injection in a SQL query WHERE section,'\
                  ' integer field which is reachable using an HTML form with'\
                  ' one parameter.'
    url_path = 'blind_where_integer_form.py'

    def post(self, request, *args, **kwds):
        # pylint: disable=E1101
        form = GenericForm(data=request.POST)
        if not form.is_valid():
            context = self.get_context_data(success=False,
                                            form=GenericForm())
        else:
            user_input = form.cleaned_data[GenericForm.INPUT]
            query = "SELECT * FROM auth_user WHERE id = %s" % user_input

            db_error, users = get_users(query)
            db_error, users = fake_error_handling(db_error, users)

            context = self.get_context_data(db_error=db_error,
                                            users=users,
                                            success=True,
                                            form=GenericForm())

        return render(request, self.template_name, context)


class BlindSQLIntegerQSView(VulnerableTemplateView):
    title = 'Trivial Blind SQL injection'
    tags = ['WHERE', 'integer', 'query-string']
    description = 'Trivial blind SQL injection in a SQL query WHERE section,'\
                  ' integer field which is reachable using a query string.'
    url_path = 'where_integer_qs.py?id=1'
    template_name = "moth/vulnerability-users-table.html"

    def get(self, request, *args, **kwds):
        user_input = request.GET.get('id', '1')
        query = "SELECT * FROM auth_user WHERE id = %s" % user_input

        db_error, users = get_users(query)
        db_error, users = fake_error_handling(db_error, users)

        context = self.get_context_data(db_error=db_error,
                                        users=users,
                                        success=True)

        return render(request, self.template_name, context)


class BlindSQLSingleQuoteStringQSView(VulnerableTemplateView):
    title = 'Trivial Blind SQL injection'
    tags = ['WHERE', 'string', 'single-quote', 'query-string']
    description = 'Trivial blind SQL injection in a SQL query WHERE section,'\
                  ' single quote string field which is reachable using a query'\
                  'string.'
    url_path = 'where_string_single_qs.py?uname=pablo'
    template_name = "moth/vulnerability-users-table.html"

    def get(self, request, *args, **kwds):
        user_input = request.GET.get('uname', 'pablo')
        query = "SELECT * FROM auth_user WHERE username = '%s'" % user_input

        db_error, users = get_users(query)
        db_error, users = fake_error_handling(db_error, users)

        context = self.get_context_data(db_error=db_error,
                                        users=users,
                                        success=True)

        return render(request, self.template_name, context)


def fake_error_handling(db_error, users):
    # Fake error handling
    if db_error:
        db_error = None
        users = []

    return db_error, users
