from moth.views.base.html_template_view import HTMLTemplateView


class HTMLInCommentView(HTMLTemplateView):
    title = 'HTML tags in HTML comment'
    description = 'HTML tags in HTML comment'
    url_path = 'html_comments/html_in_comment.html'
    
    HTML = '''
    See HTML source code.
    <!-- <b>hi!</b> -->
    '''
    
class SimpleHTMLCommentView(HTMLTemplateView):
    title = 'HTML comment'
    description = 'HTML comment'
    url_path = 'html_comments/simple_comment.html'
    
    HTML = '''
    See HTML source code.
    <!-- comment password -->
    '''