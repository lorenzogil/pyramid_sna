from pyramid_sna.oauth2 import get_user_info, oauth2_step1, oauth2_step2


def facebook_login(request):
    settings = request.registry.settings
    return oauth2_step1(
        request=request,
        auth_uri=settings['facebook_dialog_oauth_url'],
        client_id=settings['facebook_app_id'],
        redirect_url=request.route_url('facebook_callback'),
        scope=settings['facebook_scope'],
    )


def facebook_callback(request):
    settings = request.registry.settings
    access_token = oauth2_step2(
        request=request,
        token_uri=settings['facebook_access_token_url'],
        client_id=settings['facebook_app_id'],
        client_secret=settings['facebook_app_secret'],
        redirect_url=request.route_url('facebook_callback'),
        scope=settings['facebook_scope'],
    )

    info = get_user_info(settings['facebook_basic_information_url'],
                         access_token)
    user_id = info['id']
    info['screen_name'] = info['name']

    return settings['facebook_callback'](request, user_id, info)
