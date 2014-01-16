import os
import unittest

from pyramid_sna import get_available_providers, read_setting_from_env


class CallbackCounter(object):

    def __init__(self):
        self.reset()

    def __call__(self, *args, **kwargs):
        self.calls.append({'args': args, 'kwargs': kwargs})
        return 'Register success!'

    @property
    def counter(self):
        return len(self.calls)

    def reset(self):
        self.calls = []


class ConfigTests(unittest.TestCase):

    def test_read_setting_from_env(self):
        settings = {
            'foo_bar': '1',
        }

        self.assertEqual('1', read_setting_from_env(settings, 'foo_bar'))

        self.assertEqual('default',
                         read_setting_from_env(settings, 'new_option', 'default'))

        self.assertEqual(None,
                         read_setting_from_env(settings, 'new_option'))

        os.environ['FOO_BAR'] = '2'
        self.assertEqual('2', read_setting_from_env(settings, 'foo_bar'))

    def test_get_available_providers(self):
        self.assertEqual(('facebook', 'google', 'liveconnect'),
                         get_available_providers())