import os
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    config = Configurator(settings=settings)

    session_factory = SignedCookieSessionFactory('s3cr3t')
    config.set_session_factory(session_factory)

    includeme(config)

    return config.make_wsgi_app()


def read_setting_from_env(settings, key, default=None):
    env_variable = key.upper()
    if env_variable in os.environ:
        return os.environ[env_variable]
    else:
        return settings.get(key, default)


def get_available_providers():
    """Return a tuple of available providers"""
    return ('facebook', 'google', 'liveconnect')


def include_google(config):
    settings = config.registry.settings

    for key, default in (
        ('client_id', None),
        ('client_secret', None),
        ('callback', None),
        ('auth_uri', 'https://accounts.google.com/o/oauth2/auth'),
        ('token_uri', 'https://accounts.google.com/o/oauth2/token'),
        ('user_info_uri', 'https://www.googleapis.com/oauth2/v1/userinfo'),
        ('scope', 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'),
    ):

        option = 'google_%s' % key
        settings[option] = read_setting_from_env(settings, option, default)

    if (
        settings['google_client_id']
        and settings['google_client_secret']
        and settings['google_callback']
    ):

        config.add_route('google_login', '/google/login')
        config.add_view('pyramid_sna.google.google_login',
                        route_name='google_login',
                        renderer='string')

        config.add_route('google_callback', '/google/callback')
        config.add_view('pyramid_sna.google.google_callback',
                        route_name='google_callback',
                        renderer='string')

        callback = config.maybe_dotted(settings['google_callback'])
        settings['google_callback'] = callback

        return True
    else:
        return False


def include_facebook(config):
    settings = config.registry.settings

    for key, default in (
        ('app_id', None),
        ('app_secret', None),
        ('callback', None),
        ('dialog_oauth_url', 'https://www.facebook.com/dialog/oauth/'),
        ('access_token_url', 'https://graph.facebook.com/oauth/access_token'),
        ('basic_information_url', 'https://graph.facebook.com/me'),
        ('scope', 'email'),
    ):
        option = 'facebook_%s' % key
        settings[option] = read_setting_from_env(settings, option, default)

    if (
        settings['facebook_app_id']
        and settings['facebook_app_secret']
        and settings['facebook_callback']
    ):
        config.add_route('facebook_login', '/facebook/login')
        config.add_view('pyramid_sna.facebook.facebook_login',
                        route_name='facebook_login',
                        renderer='string')

        config.add_route('facebook_callback', '/facebook/callback')
        config.add_view('pyramid_sna.facebook.facebook_callback',
                        route_name='facebook_callback',
                        renderer='string')

        callback = config.maybe_dotted(settings['facebook_callback'])
        settings['facebook_callback'] = callback

        return True
    else:
        return False


def include_liveconnect(config):
    settings = config.registry.settings

    for key, default in (
        ('client_id', None),
        ('client_secret', None),
        ('callback', None),
        ('auth_uri', 'https://login.live.com/oauth20_authorize.srf'),
        ('token_uri', 'https://login.live.com/oauth20_token.srf'),
        ('basic_information_url', 'https://apis.live.net/v5.0/me'),
        ('scope', 'wl.basic wl.emails'),
    ):
        option = 'liveconnect_%s' % key
        settings[option] = read_setting_from_env(settings, option, default)

    if (
        settings['liveconnect_client_id']
        and settings['liveconnect_client_secret']
        and settings['liveconnect_callback']
    ):
        config.add_route('liveconnect_login', '/liveconnect/login')
        config.add_view('pyramid_sna.liveconnect.liveconnect_login',
                        route_name='liveconnect_login',
                        renderer='string')

        config.add_route('liveconnect_callback', '/liveconnect/callback')
        config.add_view('pyramid_sna.liveconnect.liveconnect_callback',
                        route_name='liveconnect_callback',
                        renderer='string')

        callback = config.maybe_dotted(settings['liveconnect_callback'])
        settings['liveconnect_callback'] = callback

        return True
    else:
        return False


def includeme(config):
    settings = config.registry.settings
    settings['google_auth_enabled'] = include_google(config)
    settings['facebook_auth_enabled'] = include_facebook(config)
    settings['liveconnect_auth_enabled'] = include_liveconnect(config)
