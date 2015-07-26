import unittest

from mock import patch
from webtest import TestApp

from pyramid import testing
from pyramid.request import Request

from pyramid_sna import main, include_facebook
from pyramid_sna.compat import urlparse
from pyramid_sna.tests import CallbackCounter


def example_callback(*args, **kwargs):
    pass  # pragma: no cover


class FacebookConfigTests(unittest.TestCase):

    def test_incomplete_config1(self):
        config = testing.setUp(settings={})
        self.assertFalse(include_facebook(config))
        testing.tearDown()

    def test_incomplete_config2(self):
        config = testing.setUp(settings={
            'facebook_app_id': '123',
        })
        self.assertFalse(include_facebook(config))
        testing.tearDown()

    def test_incomplete_config3(self):
        config = testing.setUp(settings={
            'facebook_app_id': '123',
            'facebook_app_secret': 's3cr3t',
        })
        self.assertFalse(include_facebook(config))
        testing.tearDown()

    def test_complete_config(self):
        config = testing.setUp(settings={
            'facebook_app_id': '123',
            'facebook_app_secret': 's3cr3t',
            'facebook_callback': example_callback,
        })
        self.assertTrue(include_facebook(config))
        testing.tearDown()


class FacebookViewTests(unittest.TestCase):

    def setUp(self):
        self.callback_counter = CallbackCounter()
        settings = {
            'facebook_app_id': '123',
            'facebook_app_secret': 's3cr3t',
            'facebook_callback': self.callback_counter,
            'facebook_scope': 'perm1 perm2',
        }
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        self.testapp.reset()

    def test_facebook_login(self):
        res = self.testapp.get('/facebook/login', {
            'next_url': 'https://localhost/foo/bar',
        })
        self.assertEqual(res.status, '302 Found')
        url = urlparse.urlparse(res.location)
        self.assertEqual(url.netloc, 'www.facebook.com')
        self.assertEqual(url.path, '/dialog/oauth/')
        query = urlparse.parse_qs(url.query)
        self.assertEqual(sorted(query.keys()), [
            'client_id', 'redirect_uri', 'response_type', 'scope', 'state',
        ])
        self.assertEqual(query['scope'], ['perm1 perm2'])
        self.assertEqual(query['redirect_uri'],
                         ['http://localhost/facebook/callback'])
        self.assertEqual(query['client_id'], ['123'])

    def test_facebook_callback(self):
        # call the login to fill the session
        res = self.testapp.get('/facebook/login', {
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
                    'username': 'john.doe',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'name': 'John Doe',
                    'email': 'john@example.com',
                }

                res = self.testapp.get('/facebook/callback', {
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
                    'id': '789',
                    'username': 'john.doe',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'name': 'John Doe',
                    'screen_name': 'John Doe',
                    'email': 'john@example.com',
                })
                call_kwargs = self.callback_counter.calls[0]['kwargs']
                self.assertEqual(call_kwargs, {})
