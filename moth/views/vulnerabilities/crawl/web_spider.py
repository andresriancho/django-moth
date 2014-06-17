from moth.views.base.html_template_view import HTMLTemplateView


class IndexView(HTMLTemplateView):
    title = 'Crawl test index page'
    url_path = 'test_case_01/'

    HTML = '''
    <a href="1.html">Start your journey</a><br/>
    '''


class OneView(HTMLTemplateView):
    title = 'Crawl test start page'
    description = 'Links to a couple of test HTMLs with different depths'
    url_path = 'test_case_01/1.html'

    HTML = '''
    <a href="2.html">Link to two</a><br/>

    <a href="a%20b.html">Link with spaces in filename</a><br/>
    <a href="d%20f/index.html">Link with spaces in path</a><br/>
    <br/>
    <br/>
    <img id=logo src='/static/moth/images/w3af.png' alt="w3af"><br/>
    <br/>
    <br/>
    <a href="../">Back</a><br/>
    '''


class TwoView(HTMLTemplateView):
    title = 'Crawl test second page'
    description = 'Links to three and four. The second tag is broken as a test.'
    url_path = 'test_case_01/2.html'
    linked = False

    HTML = '''
    <a href="3.html">Go to three</a><br/>
    <a href="4.html">Go to four</a
    '''


class ThreeView(HTMLTemplateView):
    title = 'Crawl test third page'
    description = 'Links to dead ends and loops. The second tag is broken as a test.'
    url_path = 'test_case_01/3.html'
    linked = False

    HTML = '''
    <a href="1.html">Go back to one</a>
    <br/><br/>
    img id=logo src='/static/moth/images/w3af.png' alt="w3af">
    <br/><br/>
    <a href="11.html">Dead end: 404.</a>
    '''


class FourView(HTMLTemplateView):
    title = 'Crawl test fourth page'
    description = 'Links to dead ends.'
    url_path = 'test_case_01/4.html'
    linked = False

    HTML = '''
    All dead-ends<br/>
    <a href="7.html">Dead end</a><br/>
    <a href="9.html">Dead end</a><br/>
    '''


class SpaceInPathView(HTMLTemplateView):
    title = 'Space in path'
    description = 'An index file with a space in the path'
    url_path = 'test_case_01/d f/index.html'
    linked = False

    HTML = '''
    I do exist.
    '''


class SpaceInFileView(HTMLTemplateView):
    title = 'Space in filename'
    description = 'A file with a space'
    url_path = 'test_case_01/a b.html'
    linked = False

    HTML = '''
    I do exist.
    '''