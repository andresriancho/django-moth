import urlparse

from moth.views.base.html_template_view import HTMLTemplateView


class RawPathTemplateView(HTMLTemplateView):
    """
    A view that has a raw URL path and has fixed HTML body.
    """
    HTML = None

    def get_url_path(self):
        '''
        We can locate this view in any directory. Other views that don't inherit
        from RawPathTemplateView will get located in a well structured location
        '''
        path = urlparse.urlparse(self.url_path).path
        return unicode('%s' % path)

    # FIXME: Add support for encoding
    get_unicode_url_path = get_url_path