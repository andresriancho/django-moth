from django.contrib.auth.models import User
from django.shortcuts import render

from moth.forms.generic import GenericForm
from moth.views.base.form_template_view import FormTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class SQLIntegerFormView(FormTemplateView):
    template_name = "moth/vulnerability-users-table.html"
    title = 'Trivial SQL injection: (WHERE|integer|form)'
    description = 'Trivial SQL injection in a SQL query WHERE section, integer'\
                  ' field which is reachable using an HTML form with one'\
                  ' parameter.'
    url_path = 'where_integer_form.py'
    
    def post(self, request, *args, **kwds):
        form = GenericForm(data=request.POST)
        if not form.is_valid():
            context = self.get_context_data(success=False,
                                            form=GenericForm())
        else:
            user_input = form.cleaned_data[GenericForm.INPUT]
            db_error, users = sql_injection_where_integer(user_input)
            
            context = self.get_context_data(db_error=db_error,
                                            users=users,
                                            success=True,
                                            form=GenericForm())
            
        return render(request, self.template_name, context)

class SQLIntegerQSView(VulnerableTemplateView):
    title = 'Trivial SQL injection: (WHERE|integer|query-string)'
    description = 'Trivial SQL injection in a SQL query WHERE section, integer'\
                  ' field which is reachable using a query string.'
    url_path = 'where_integer_qs.py?id=1'
    template_name = "moth/vulnerability-users-table.html"
    
    def get(self, request, *args, **kwds):
        user_input = request.GET['id']
        db_error, users = sql_injection_where_integer(user_input)
        
        context = self.get_context_data(db_error=db_error,
                                        users=users,
                                        success=True)
        
        return render(request, self.template_name, context)

def sql_injection_where_integer(user_input):
    users = None
    db_error = None
    
    query = "SELECT * FROM auth_user WHERE id = %s" % user_input
    
    try:
        users_qs = User.objects.raw(query)
        users = [u for u in users_qs]
    except Exception, dbe:
        db_error = str(dbe)
    
    return db_error, users

# String WHERE
# query = "SELECT * FROM auth_user WHERE username = '%s'" % user_input