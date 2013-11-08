from django.test import TestCase


class RouterTestCase(TestCase):
    def test_routes_grep(self):
        response = self.client.get('/event_validation/event_validation.html')
        
        self.assertIn('.NET Event validation', response.content)
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/vulnerability.html')
    
    def test_index_of(self):
        response = self.client.get('/event_validation/')
        
        self.assertIn('Event Validation test suite', response.content)
        self.assertIn('(secure)', response.content)
        self.assertIn('(insecure)', response.content)
        
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/index-of.html')
