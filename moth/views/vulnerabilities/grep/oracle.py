from moth.views.base.html_template_view import HTMLTemplateView


class CreatedByOracleView(HTMLTemplateView):
    title = 'Created by Oracle'
    description = 'Created by Oracle HTML comment'
    url_path = 'oracle/created_by_oracle.html'
    
    HTML = '''<!-- Created by Oracle -->'''
