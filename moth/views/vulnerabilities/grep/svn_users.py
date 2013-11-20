from moth.views.base.html_template_view import HTMLTemplateView


class SVNUsersView(HTMLTemplateView):
    title = 'SVN users in HTML tags'
    description = 'SVN users in HTML comment tags'
    url_path = 'svn_users/index.html'
    
    HTML = '''$Horde: framework/VC/VC/svn.php,v 1.28.4.18 2006/05/12 04:47:08 chuck Exp $'''
