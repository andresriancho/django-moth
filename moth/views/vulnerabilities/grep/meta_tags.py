from moth.views.base.html_template_view import HTMLTemplateView


class MetaTagsGoogleView(HTMLTemplateView):
    title = 'Meta tags added by google sitemap'
    description = 'See HTML source to find Google verification meta tag'
    url_path = 'google_sitemap.html'
    
    HTML = '''
    See HTML source
    <meta name="verify-v1" content="/JBoXnwT1d7TbbWCwL8tXe+Ts2I2LXYrdnnK50g7kdY=" />
    '''

class MetaTagsLinuxView(HTMLTemplateView):
    title = 'Meta tag with "linux" inside'
    description = 'See HTML source to find a meta tag that says "linux"'
    url_path = 'linux_meta.html'
    
    HTML = '''
    See HTML source
    <meta name="foo" content="linux only page" />
    '''
