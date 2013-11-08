from django.test import TestCase


class SiteTestCase(TestCase):
    def test_home(self):
        response = self.client.get('/')
        
        self.assertIn('A set of vulnerable scripts', response.content)
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/home.html')
        
    def test_about(self):
        response = self.client.get('/about/')
        
        self.assertIn('This software is the evolution', response.content)
        self.assertTemplateUsed(response, 'moth/base.html')
        self.assertTemplateUsed(response, 'moth/about.html')