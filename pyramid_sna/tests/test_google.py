import unittest

from mock import patch
from webtest import TestApp

from pyramid import testing
from pyramid.request import Request

from pyramid_sna import main, include_google
from pyramid_sna.compat import urlparse
from pyramid_sna.tests import CallbackCounter


def example_callback(*args, **kwargs):
    pass  # pragma: no cover


class GoogleConfigTests(unittest.TestCase):

    def test_incomplete_config1(self):
        config = testing.setUp(settings={})
        self.assertFalse(include_google(config))
        testing.tearDown()

    def test_incomplete_config2(self):
        config = testing.setUp(settings={
            'google_client_id': '123',
        })
        self.assertFalse(include_google(config))
        testing.tearDown()

    def test_incomplete_config3(self):
        config = testing.setUp(settings={
            'google_client_id': '123',
            'google_client_secret': 's3cr3t',
        })
        self.assertFalse(include_google(config))
        testing.tearDown()

    def test_complete_config(self):
        config = testing.setUp(settings={
            'google_client_id': '123',
            'google_client_secret': 's3cr3t',
            'google_callback': example_callback,
        })
        self.assertTrue(include_google(config))
        testing.tearDown()


class GoogleViewTests(unittest.TestCase):

    def setUp(self):
        self.callback_counter = CallbackCounter()
        settings = {
            'google_client_id': '123',
            'google_client_secret': 's3cr3t',
            'google_callback': self.callback_counter,
            'google_scope': 'perm1 perm2',
        }
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        self.testapp.reset()

    def test_google_login(self):
        res = self.testapp.get('/google/login', {
            'next_url': 'https://localhost/foo/bar',
        })
        self.assertEqual(res.status, '302 Found')
        url = urlparse.urlparse(res.location)
        self.assertEqual(url.netloc, 'accounts.google.com')
        self.assertEqual(url.path, '/o/oauth2/auth')
        query = urlparse.parse_qs(url.query)
        self.assertEqual(sorted(query.keys()), [
            'client_id', 'redirect_uri', 'response_type', 'scope', 'state',
        ])
        self.assertEqual(query['scope'], ['perm1 perm2'])
        self.assertEqual(query['redirect_uri'],
                         ['http://localhost/google/callback'])
        self.assertEqual(query['client_id'], ['123'])

    def test_google_callback(self):
        # call the login to fill the session
        res = self.testapp.get('/google/login', {
            'next_url': 'https://localhost/foo/bar',
        })
        self.assertEqual(res.status, '302 Found')
        url = urlparse.urlparse(res.location)
        query = urlparse.parse_qs(url.query)
        state = query['state'][0]

        with patch('requests.post') as fake_post:
            fake_post.return_value.status_code = 200
            fake_post.return_value.json = lambda: {
                'access_token': '1234',
            }
            with patch('requests.get') as fake_get:
                fake_get.return_value.status_code = 200
                fake_get.return_value.json = lambda: {
                    'id': '789',
                    'name': 'John Doe',
                    'given_name': 'John',
                    'family_name': 'Doe',
                    'email': 'john@example.com',
                }

                res = self.testapp.get('/google/callback', {
                    'code': '1234',
                    'state': state,
                })
                self.assertEqual(res.status, '200 OK')
                self.assertEqual(res.text, 'Register success!')

                self.assertEqual(self.callback_counter.counter, 1)
                call_args = self.callback_counter.calls[0]['args']
                self.assertTrue(isinstance(call_args[0], Request))
                self.assertEqual(call_args[1], '789')
                self.assertEqual(call_args[2], {
                    'email': 'john@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'screen_name': 'John Doe',
                })
                call_kwargs = self.callback_counter.calls[0]['kwargs']
                self.assertEqual(call_kwargs, {})
