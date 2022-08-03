# -*- coding: utf-8 -*-
#
import requests

from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from django.conf import settings
from django.urls import reverse

from common.utils import get_logger
from users.utils import construct_user_email
from authentication.utils import build_absolute_uri
from common.exceptions import JMSException

from .signals import (
    oauth2_create_or_update_user, oauth2_user_login_failed,
    oauth2_user_login_success
)
from ..base import JMSModelBackend


__all__ = ['OAuth2Backend']

logger = get_logger(__name__)


class OAuth2Backend(JMSModelBackend):
    @staticmethod
    def is_enabled():
        return settings.AUTH_OAUTH2

    def get_or_create_user_from_userinfo(self, request, userinfo):
        log_prompt = "Get or Create user [OAuth2Backend]: {}"
        logger.debug(log_prompt.format('start'))

        # Construct user attrs value
        user_attrs = {}
        for field, attr in settings.AUTH_OAUTH2_USER_ATTR_MAP.items():
            user_attrs[field] = userinfo.get(attr, '')

        username = user_attrs.get('username')
        if not username:
            error_msg = 'username is missing'
            logger.error(log_prompt.format(error_msg))
            raise JMSException(error_msg)

        email = user_attrs.get('email', '')
        email = construct_user_email(user_attrs.get('username'), email)
        user_attrs.update({'email': email})

        logger.debug(log_prompt.format(user_attrs))
        user, created = get_user_model().objects.get_or_create(
            username=username, defaults=user_attrs
        )
        logger.debug(log_prompt.format("user: {}|created: {}".format(user, created)))
        logger.debug(log_prompt.format("Send signal => oauth2 create or update user"))
        oauth2_create_or_update_user.send(
            sender=self.__class__, request=request, user=user, created=created,
            attrs=user_attrs
        )
        return user, created

    @staticmethod
    def get_response_data(response_data):
        if response_data.get('data') is not None:
            response_data = response_data['data']
        return response_data

    @staticmethod
    def get_query_dict(response_data, query_dict):
        query_dict.update({
            'uid': response_data.get('uid', ''),
            'access_token': response_data.get('access_token', '')
        })
        return query_dict

    def authenticate(self, request, code=None, **kwargs):
        log_prompt = "Process authenticate [OAuth2Backend]: {}"
        logger.debug(log_prompt.format('Start'))
        if code is None:
            logger.error(log_prompt.format('code is missing'))
            return None

        query_dict = {
            'client_id': settings.AUTH_OAUTH2_CLIENT_ID,
            'client_secret': settings.AUTH_OAUTH2_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': build_absolute_uri(
                request, path=reverse(settings.AUTH_OAUTH2_AUTH_LOGIN_CALLBACK_URL_NAME)
            )
        }
        access_token_url = '{url}?{query}'.format(
            url=settings.AUTH_OAUTH2_ACCESS_TOKEN_ENDPOINT, query=urlencode(query_dict)
        )
        token_method = settings.AUTH_OAUTH2_ACCESS_TOKEN_METHOD.lower()
        requests_func = getattr(requests, token_method, requests.get)
        logger.debug(log_prompt.format('Call the access token endpoint[method: %s]' % token_method))
        headers = {
            'Accept': 'application/json'
        }
        access_token_response = requests_func(access_token_url, headers=headers)
        try:
            access_token_response.raise_for_status()
            access_token_response_data = access_token_response.json()
            response_data = self.get_response_data(access_token_response_data)
        except Exception as e:
            error = "Json access token response error, access token response " \
                    "content is: {}, error is: {}".format(access_token_response.content, str(e))
            logger.error(log_prompt.format(error))
            return None

        query_dict = self.get_query_dict(response_data, query_dict)

        headers = {
            'Accept': 'application/json',
            'Authorization': 'token {}'.format(response_data.get('access_token', ''))
        }

        logger.debug(log_prompt.format('Get userinfo endpoint'))
        userinfo_url = '{url}?{query}'.format(
            url=settings.AUTH_OAUTH2_PROVIDER_USERINFO_ENDPOINT,
            query=urlencode(query_dict)
        )
        userinfo_response = requests.get(userinfo_url, headers=headers)
        try:
            userinfo_response.raise_for_status()
            userinfo_response_data = userinfo_response.json()
            if 'data' in userinfo_response_data:
                userinfo = userinfo_response_data['data']
            else:
                userinfo = userinfo_response_data
        except Exception as e:
            error = "Json userinfo response error, userinfo response " \
                    "content is: {}, error is: {}".format(userinfo_response.content, str(e))
            logger.error(log_prompt.format(error))
            return None

        try:
            logger.debug(log_prompt.format('Update or create oauth2 user'))
            user, created = self.get_or_create_user_from_userinfo(request, userinfo)
        except JMSException:
            return None

        if self.user_can_authenticate(user):
            logger.debug(log_prompt.format('OAuth2 user login success'))
            logger.debug(log_prompt.format('Send signal => oauth2 user login success'))
            oauth2_user_login_success.send(sender=self.__class__, request=request, user=user)
            return user
        else:
            logger.debug(log_prompt.format('OAuth2 user login failed'))
            logger.debug(log_prompt.format('Send signal => oauth2 user login failed'))
            oauth2_user_login_failed.send(
                sender=self.__class__, request=request, username=user.username,
                reason="User is invalid"
            )
            return None
