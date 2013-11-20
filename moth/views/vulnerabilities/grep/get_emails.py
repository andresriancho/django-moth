from moth.views.base.html_template_view import HTMLTemplateView


class GetEmailsView(HTMLTemplateView):
    title = 'Page with lots of emails'
    description = 'Page with a ton of different emails, false positive checks'\
                  ' email formats, encodings, separators, etc.'
    url_path = 'emails.html'
    
    HTML = '''
    <html>
    Test various email separator characters <br />
    %20f00@moth.com
                    bar@moth.com
             hello@world.com
    
    <br/><br />Test URL encoded emails: <br />
    hello%20world@f00.net
    
    <br/><br />Test email with invalid URL encode: <br />
            hello%planer@moth.com
    
    <br/><br />Test email with invalid URL encode: <br />
    andres@moth , please note that this email address won't be found because it
    doesn't match the regular expression we use to find emails, which requires
    the domain part to have at least a dot (.).
    
    <br /><br />Test mailto tag: <br />
    %20%20%20%20<mailto href="pp@moth.com">
    
    <br /><br />Test misc:<br/>
            notMe!@gmail.com
            notMe@gmail.com pleaseMe@moth
    
    <br /><br />Test HTML encoded:<br/>
    ramosmejia_direcci&oacute;n@moth
    </html>
    '''