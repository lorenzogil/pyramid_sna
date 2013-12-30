import uuid

import requests

from pyramid.httpexceptions import HTTPBadRequest, HTTPFound, HTTPUnauthorized

from pyramid_sna.compat import urlparse, url_encode


def oauth2_step1(request, auth_uri, client_id, redirect_url, scope):
    state = str(uuid.uuid4())
    request.session['state'] = state

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_url,
        'scope': scope,
        'state': state,
    }

    if 'next_url' in request.params:
        request.session['next_url'] = request.params['next_url']

    return HTTPFound(location=auth_uri + '?' + url_encode(params))


def oauth2_step2(request, token_uri, client_id, client_secret, redirect_url,
                 scope):
    try:
        code = request.params['code']
    except KeyError:
        return HTTPBadRequest('Missing required code')

    try:
        state = request.params['state']
    except KeyError:
        return HTTPBadRequest('Missing required state')

    try:
        my_state = request.session['state']
        if state != my_state:
            return HTTPUnauthorized('State parameter does not match internal '
                                    'state. You may be a victim of CSRF')
        else:
            del request.session['state']
    except KeyError:
        return HTTPUnauthorized('Missing internal state. '
                                'You may be a victim of CSRF')

    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_url,
        'scope': scope,
    }

    response = requests.post(token_uri, data=params)

    if response.status_code != 200:
        return HTTPUnauthorized(response.text)

    try:
        response_dict = response.json()
    except ValueError:
        response_dict = dict(urlparse.parse_qsl(response.text))

    return response_dict['access_token']


def get_user_info(info_uri, access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    response = requests.get(info_uri, headers=headers)

    if response.status_code != 200:
        raise HTTPUnauthorized(response.text)

    return response.json()
