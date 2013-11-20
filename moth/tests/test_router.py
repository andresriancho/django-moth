from django.test import TestCase


class RouterTestCase(TestCase):
    def test_routes_grep(self):
        response = self.client.get('/grep/event_validation/event_validation.html')
        
        self.assertIn('.NET Event validation', response.content)
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/vulnerability.html')
    
    def test_index_of(self):
        response = self.client.get('/grep/event_validation/')
        
        self.assertIn('Event Validation test suite', response.content)
        self.assertIn('(secure)', response.content)
        self.assertIn('(insecure)', response.content)
        
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/index-of.html')
        
        self.assertNotIn('cross_domain_script_with_type.html', response.content)

    def test_family_index_of(self):
        response = self.client.get('/grep/')
        
        self.assertIn('Event validation', response.content)
        self.assertIn('DOM XSS', response.content)
        
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/index-of-family.html')
        
        self.assertNotIn('simple_xss.py', response.content)

    def test_links_with_params(self):
        '''
        Want to make sure that the router supports links with query string
        parameters.
        '''
        response = self.client.get('/audit/')
        self.assertIn('xss/simple_xss.py?text=1', response.content)
        
        response = self.client.get('/audit/xss/simple_xss.py?text=foobar123')
        self.assertIn('foobar123', response.content)
        