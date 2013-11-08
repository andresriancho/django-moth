from moth.views.base.html_template_view import HTMLTemplateView


class DotNetWithEVView(HTMLTemplateView):
    title = '.NET Event validation'
    description = 'With VIEWSTATE and EVENTVALIDATION'
    url_path = 'event_validation/'
    file_pattern = 'event_validation.html'
    
    HTML = '''
    <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUKLTMyNjg0MDc1MWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFIGJwJF8kY3RsMDAkXyRicyRfJHdzJF8kU2VhcmNoQm94bxUzDQVBRPB2cN8nnSmNhVZ6WX0=" />
    <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWAgKvz4izBwKM54rGBiEhTsyhLU3XkVd490N5C2TbyVCW" />
    '''
