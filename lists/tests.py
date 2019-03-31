from django.test import TestCase

class SmokeTest(TestCase):
    
    def test_bad_math(self):
        self.assertEqual(2 +2, 5)
