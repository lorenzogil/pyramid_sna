from pyramid_sna.oauth2 import get_user_info, oauth2_step1, oauth2_step2


def liveconnect_login(request):
    settings = request.registry.settings
    return oauth2_step1(
        request=request,
        auth_uri=settings['liveconnect_auth_uri'],
        client_id=settings['liveconnect_client_id'],
        redirect_url=request.route_url('liveconnect_callback'),
        scope=settings['liveconnect_scope'],
    )


def liveconnect_callback(request):
    settings = request.registry.settings
    access_token = oauth2_step2(
        request=request,
        token_uri=settings['liveconnect_token_uri'],
        client_id=settings['liveconnect_client_id'],
        client_secret=settings['liveconnect_client_secret'],
        redirect_url=request.route_url('liveconnect_callback'),
        scope=settings['liveconnect_scope'],
    )

    info = get_user_info(settings['liveconnect_basic_information_url'],
                         access_token)
    user_id = info['id']
    info['screen_name'] = info.get('name', '')
    if 'wl.emails' in settings['liveconnect_scope']:
        info['email'] = info.get('emails', {}).get('account', '')

    return settings['liveconnect_callback'](request, user_id, info)
