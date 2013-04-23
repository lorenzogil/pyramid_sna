from pyramid_sna.oauth2 import get_user_info, oauth2_step1, oauth2_step2


def google_login(request):
    settings = request.registry.settings
    return oauth2_step1(
        request=request,
        auth_uri=settings['google_auth_uri'],
        client_id=settings['google_client_id'],
        redirect_url=request.route_url('google_callback'),
        scope=settings['google_scope'],
    )


def google_callback(request):
    settings = request.registry.settings
    access_token = oauth2_step2(
        request=request,
        token_uri=settings['google_token_uri'],
        client_id=settings['google_client_id'],
        client_secret=settings['google_client_secret'],
        redirect_url=request.route_url('google_callback'),
        scope=settings['google_scope'],
    )

    info = get_user_info(settings['google_user_info_uri'], access_token)
    user_id = info['id']
    new_info = {
        'screen_name': info.get('name', ''),
        'first_name': info.get('given_name', ''),
        'last_name': info.get('family_name', ''),
        'email': info.get('email', ''),
    }

    return settings['google_callback'](request, user_id, new_info)
