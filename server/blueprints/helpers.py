# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, g
import traceback
from utils.helpers import now, pre_process_scope
from apiresps.errors import AuthFailed


def verify_token():
    ExtUser = current_app.mongodb_conn.ExtUser

    # fake data
    #
    # user = ExtUser.find_one()
    # if not user:
    #     user = ExtUser()
    #     user['scope'] = u'tester/testapp'
    #     user['open_id'] = u'test-open-id'
    #     user.save()
    # g.curr_user = user
    #
    # return

    open_id = current_app.sup_oauth.load_ext_token(request.headers)

    if not open_id:
        raise AuthFailed('invalid open id')

    user = ExtUser.find_one_activated_by_open_id(open_id)
    if user is None:
        raise AuthFailed("User Not Exist")

    if not user['access_token'] or user['expires_at'] < now():
        try:
            assert bool(user['refresh_token'])
            resp = current_app.sup_oauth.\
                refresh_access_token(user['refresh_token'])
            assert 'access_token' in resp
        except Exception:
            current_app.logger.warn(
                "Refresh token failed:\n{}".format(traceback.format_exc()))
            raise AuthFailed('refresh token failed')

        try:
            profile = current_app.sup_oauth.\
                get_profile(resp['access_token'])
        except:
            profile = None

        user['access_token'] = resp['access_token']
        user['expires_at'] = resp['expires_in'] + now()
        user['owner'] = resp['owner']
        user['app'] = resp['app']
        user['token_type'] = resp['token_type']

        if profile:
            user['display_name'] = profile['display_name']
            user['title'] = profile['title']
            user['locale'] = profile['locale']
            user['description'] = profile['description']
            user['type'] = profile['type']
            user['snapshot'] = profile['snapshot']
            user['scope'] = pre_process_scope(profile['owner_alias'],
                                              profile['app_alias'])
        user.save()

    g.curr_user = user
