import unittest

from mock import patch

from pyramid.testing import DummyRequest

from pyramid_sna.compat import urlparse
from pyramid_sna.oauth2 import get_user_info, oauth2_step1, oauth2_step2


class Oauth2ClientTests(unittest.TestCase):

    def test_oauth2_step1(self):
        with patch('uuid.uuid4') as fake:
            fake.return_value = 'random-string'

            request = DummyRequest()
            request.params = {'next_url': 'http://localhost/'}
            request.session = {}
            response = oauth2_step1(
                request=request,
                auth_uri='http://example.com/oauth2/auth',
                client_id='1234',
                redirect_url='http://localhost/oauth2/callback',
                scope='scope1 scope2'
            )
            self.assertEqual(response.status, '302 Found')
            url = urlparse.urlparse(response.location)
            self.assertEqual(url.netloc, 'example.com')
            self.assertEqual(url.path, '/oauth2/auth')
            query = urlparse.parse_qs(url.query)
            self.assertEqual(query, {
                'scope': ['scope1 scope2'],
                'state': ['random-string'],
                'redirect_uri': ['http://localhost/oauth2/callback'],
                'response_type': ['code'],
                'client_id': ['1234'],
            })
            self.assertEqual(request.session['next_url'], 'http://localhost/')

    def test_oauth2_step2(self):
        token_uri = 'http://example.com/oauth2/token'
        client_id = '1234'
        client_secret = 'secret'
        redirect_url = 'http://localhost/oauth2/callback'
        scope = 'scope1 scope2'
        request = DummyRequest()
        response = oauth2_step2(request, token_uri, client_id, client_secret,
                                redirect_url, scope)
        self.assertEqual(response.status, '400 Bad Request')
        self.assertEqual(response.message, 'Missing required code')

        request.params = {'code': 'abcdef'}
        response = oauth2_step2(request, token_uri, client_id, client_secret,
                                redirect_url, scope)
        self.assertEqual(response.status, '400 Bad Request')
        self.assertEqual(response.message, 'Missing required state')

        request.params['state'] = 'random-string'
        response = oauth2_step2(request, token_uri, client_id, client_secret,
                                redirect_url, scope)
        self.assertEqual(response.status, '401 Unauthorized')
        self.assertEqual(response.message, 'Missing internal state. You may be a victim of CSRF')

        request.session = {'state': 'other-string'}
        response = oauth2_step2(request, token_uri, client_id, client_secret,
                                redirect_url, scope)
        self.assertEqual(response.status, '401 Unauthorized')
        self.assertEqual(response.message, 'State parameter does not match internal state. You may be a victim of CSRF')

        with patch('requests.post') as fake:
            fake.return_value.status_code = 401
            fake.return_value.text = 'Unauthorized request'
            request.session['state'] = 'random-string'
            response = oauth2_step2(request, token_uri,
                                    client_id, client_secret,
                                    redirect_url, scope)
            self.assertEqual(response.status, '401 Unauthorized')
            self.assertEqual(response.message, 'Unauthorized request')

        with patch('requests.post') as fake:
            fake.return_value.status_code = 200
            fake.return_value.json = lambda: {
                'access_token': 'qwerty'
            }
            request.session['state'] = 'random-string'
            response = oauth2_step2(request, token_uri,
                                    client_id, client_secret,
                                    redirect_url, scope)
            self.assertEqual(response, 'qwerty')

        with patch('requests.post') as fake:
            fake.return_value.status_code = 200
            def non_valid_json():
                raise ValueError()
            fake.return_value.json = non_valid_json
            fake.return_value.text = 'access_token=qwerty'
            request.session['state'] = 'random-string'
            response = oauth2_step2(request, token_uri,
                                    client_id, client_secret,
                                    redirect_url, scope)
            self.assertEqual(response, 'qwerty')

    def test_get_user_info(self):
        from pyramid.httpexceptions import HTTPUnauthorized
        with patch('requests.get') as fake:
            fake.return_value.status_code = 401
            fake.return_value.text = 'Unauthorized request'

            self.assertRaises(HTTPUnauthorized, get_user_info,
                              'http://example.com/info', 'qwerty')

        with patch('requests.get') as fake:
            fake.return_value.status_code = 200
            fake.return_value.json = lambda: {
                'name': 'John',
                'surname': 'Doe',
            }

            response = get_user_info('http://example.com/info', 'qwerty')
            self.assertEqual(response, {
                'name': 'John',
                'surname': 'Doe',
            })
