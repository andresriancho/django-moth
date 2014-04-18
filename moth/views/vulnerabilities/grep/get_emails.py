from moth.views.base.html_template_view import HTMLTemplateView


class GetEmailsView(HTMLTemplateView):
    title = 'Page with lots of emails'
    description = 'Page with a ton of different emails, false positive checks'\
                  ' email formats, encodings, separators, etc. Keep in mind'\
                  ' that w3af will only extract emails in "a" tags with'\
                  ' "mailto:" protocol (for performance reasons).'
    url_path = 'emails.html'
    
    HTML = '''
    <html>
    Simplest cases:<br />
        <ul>
            <li><a href="mailto:one@moth.com">test</a></li>
            <li><a href="mailto:two@moth.com?subject=hello">test</a></li>
        <ul>

    Test various email separator characters:<br />
        <ul>
            <li><a href="mailto:%20three@moth.com">test</a></li>
            <li><a href="mailto: four@moth.com">test</a></li>
        <ul>

    Test invalid email addresses:<br />
        <ul>
            <li><a href="mailto:false!@moth.com">test</a></li>
            <li><a href="mailto:false@@moth.com">test</a></li>
        <ul>
    '''