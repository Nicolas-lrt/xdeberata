from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import sign_in


class TestUrls(SimpleTestCase):

    def test_sign_in_url_is_resolved(self):
        url = reverse('sign_in')
        print(resolve(url))
        self.assertEquals(resolve(url).func, sign_in)
