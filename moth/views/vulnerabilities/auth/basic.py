import base64

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render

from moth.views.base.html_template_view import HTMLTemplateView

#
# basic authentication code from https://djangosnippets.org/snippets/243/
#
# Modified to avoid using django's authentication system and just use
# my configuration parameters here in this file.
#
def view_or_basicauth(view, request, users, realm = "", *args, **kwargs):
    """
    This is a helper function used by both 'logged_in_or_basicauth' and
    'has_perm_or_basicauth' that does the nitty of determining if they
    are already logged in or if they have provided proper http-authorization
    and returning the view if all goes well, otherwise responding with a 401.
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                print uname, passwd, users
                if (uname, passwd) in users:
                    return view(request, *args, **kwargs)

    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 401
    # back to them to ask them to authenticate.
    #
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response
    

def logged_in_or_basicauth(users=(), realm = ""):
    """
    A simple decorator that requires a user to be logged in. If they are not
    logged in the request is examined for a 'authorization' header.

    If the header is present it is tested for basic authentication and
    the user is logged in with the provided credentials.

    If the header is not present a http 401 is sent back to the
    requestor to provide credentials.

    The purpose of this is that in several django projects I have needed
    several specific views that need to support basic authentication, yet the
    web site as a whole used django's provided authentication.

    The uses for this are for urls that are access programmatically such as
    by rss feed readers, yet the view requires a user to be logged in. Many rss
    readers support supplying the authentication credentials via http basic
    auth (and they do NOT support a redirect to a form where they post a
    username/password.)

    Use is simple:

    @logged_in_or_basicauth
    def your_view:
        ...

    You can provide the name of the realm to ask for authentication within.
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request,
                                     users, realm, *args, **kwargs)
        return wrapper
    return view_decorator


class BasicHttpAuthenticatedView(HTMLTemplateView):
    title = 'Basic HTTP authentication'
    tags = ['guessable', 'trivial', 'admin']
    description = 'Access with HTTP basic authentication with weak credentials'
    url_path = 'weak/'
    users = (('admin', 'admin'),)
    
    HTML = '''Authentication success!'''
    
    @method_decorator(logged_in_or_basicauth(users=users, realm='Trivial'))
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = self.HTML
        return render(request, self.template_name, context)


class BasicHttpImpossibleAuthenticatedView(HTMLTemplateView):
    title = 'Basic HTTP authentication'
    tags = ['impossible', 'not guessable']
    description = 'Access with HTTP basic authentication with hard to guess'\
                  ' credentials.'
    url_path = 'impossible/'
    false_positive_check = True
    users = (('admin', 'ad2m1a0dm0in5i7n'),)
    
    HTML = '''Authentication success!'''
    
    @method_decorator(logged_in_or_basicauth(users=users, realm='Impossible'))
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = self.HTML
        return render(request, self.template_name, context)
