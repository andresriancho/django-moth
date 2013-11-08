from django.test import TestCase


class RouterTestCase(TestCase):
    def test_routes_grep(self):
        response = self.client.get('/event_validation/event_validation.html')
        
        self.assertIn('.NET Event validation', response.content)
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/vulnerability.html')