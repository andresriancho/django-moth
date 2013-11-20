from moth.views.base.html_template_view import HTMLTemplateView


class CreditCardsView(HTMLTemplateView):
    title = 'Page containing credit card number'
    description = 'Page containing credit card number'
    url_path = 'cc.html'
    
    #TODO: Review, what about the 3b at the beginning? Just migrated it without
    #      checking if the test on the w3af site passes or not.
    HTML = '''3b71449635402848'''

class FPCreditCardsView(HTMLTemplateView):
    title = 'False positive check for credit card number'
    description = 'False positive check with strings that look like CCs.'
    url_path = 'false-positive-cc.html'
    false_positive_check = True
    
    HTML = '''_c3E6E547C-BFB7-4897-86EA-882A04BDE274_kDF867BE9-DEC5-0FFF-6629-127552370B17'''
