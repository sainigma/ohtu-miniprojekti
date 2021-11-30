import unittest

from requests.api import get
from services.url_validator import *

class UrlValidatorTest(unittest.TestCase):
    def setUp(self):
      pass

    def test_invalid_url_returns_none(self):
      invalidUrls = [
        'httpf://www.gasdf.com',
        'https://www. asd.com',
        'http://www.fkdjsf.com/ jotain',
        ''
      ]
      for invalidUrl in invalidUrls:
        self.assertEqual(get_url(invalidUrl), None)

    def test_valid_url_returns_dict(self):
      validUrls = [
        'https://www.google.com',
        'http://www.altavista.com'
      ]
      for validUrl in validUrls:
        response = get_url(validUrl)
        self.assertEqual(response['status'], 200)