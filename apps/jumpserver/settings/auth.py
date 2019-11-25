# -*- coding: utf-8 -*-
#
import os
import ldap
from django.urls import reverse_lazy

from ..const import CONFIG, DYNAMIC, PROJECT_DIR

# OTP settings
OTP_ISSUER_NAME = CONFIG.OTP_ISSUER_NAME
OTP_VALID_WINDOW = CONFIG.OTP_VALID_WINDOW

# Auth LDAP settings
AUTH_LDAP = DYNAMIC.AUTH_LDAP
AUTH_LDAP_SERVER_URI = DYNAMIC.AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = DYNAMIC.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = DYNAMIC.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_SEARCH_OU = DYNAMIC.AUTH_LDAP_SEARCH_OU
AUTH_LDAP_SEARCH_FILTER = DYNAMIC.AUTH_LDAP_SEARCH_FILTER
AUTH_LDAP_START_TLS = DYNAMIC.AUTH_LDAP_START_TLS
AUTH_LDAP_USER_ATTR_MAP = DYNAMIC.AUTH_LDAP_USER_ATTR_MAP
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_REFERRALS: CONFIG.AUTH_LDAP_OPTIONS_OPT_REFERRALS
}
LDAP_CERT_FILE = os.path.join(PROJECT_DIR, "data", "certs", "ldap_ca.pem")
if os.path.isfile(LDAP_CERT_FILE):
    AUTH_LDAP_GLOBAL_OPTIONS[ldap.OPT_X_TLS_CACERTFILE] = LDAP_CERT_FILE
# AUTH_LDAP_GROUP_SEARCH_OU = CONFIG.AUTH_LDAP_GROUP_SEARCH_OU
# AUTH_LDAP_GROUP_SEARCH_FILTER = CONFIG.AUTH_LDAP_GROUP_SEARCH_FILTER
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#    AUTH_LDAP_GROUP_SEARCH_OU, ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_SEARCH_FILTER
# )
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_TIMEOUT: CONFIG.AUTH_LDAP_CONNECT_TIMEOUT
}
AUTH_LDAP_CACHE_TIMEOUT = 1
AUTH_LDAP_ALWAYS_UPDATE_USER = True

AUTH_LDAP_SEARCH_PAGED_SIZE = CONFIG.AUTH_LDAP_SEARCH_PAGED_SIZE
AUTH_LDAP_SYNC_IS_PERIODIC = CONFIG.AUTH_LDAP_SYNC_IS_PERIODIC
AUTH_LDAP_SYNC_INTERVAL = CONFIG.AUTH_LDAP_SYNC_INTERVAL
AUTH_LDAP_SYNC_CRONTAB = CONFIG.AUTH_LDAP_SYNC_CRONTAB
AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS = CONFIG.AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS

# openid
# Auth OpenID settings
BASE_SITE_URL = CONFIG.BASE_SITE_URL
AUTH_OPENID = CONFIG.AUTH_OPENID
AUTH_OPENID_SERVER_URL = CONFIG.AUTH_OPENID_SERVER_URL
AUTH_OPENID_REALM_NAME = CONFIG.AUTH_OPENID_REALM_NAME
AUTH_OPENID_CLIENT_ID = CONFIG.AUTH_OPENID_CLIENT_ID
AUTH_OPENID_CLIENT_SECRET = CONFIG.AUTH_OPENID_CLIENT_SECRET
AUTH_OPENID_IGNORE_SSL_VERIFICATION = CONFIG.AUTH_OPENID_IGNORE_SSL_VERIFICATION
AUTH_OPENID_SHARE_SESSION = CONFIG.AUTH_OPENID_SHARE_SESSION
AUTH_OPENID_LOGIN_URL = reverse_lazy("authentication:")
AUTH_OPENID_LOGIN_COMPLETE_URL = reverse_lazy("authentication:openid:openid-login-complete")


# Radius Auth
AUTH_RADIUS = CONFIG.AUTH_RADIUS
AUTH_RADIUS_BACKEND = 'authentication.backends.radius.RadiusBackend'
RADIUS_SERVER = CONFIG.RADIUS_SERVER
RADIUS_PORT = CONFIG.RADIUS_PORT
RADIUS_SECRET = CONFIG.RADIUS_SECRET


TOKEN_EXPIRATION = CONFIG.TOKEN_EXPIRATION
LOGIN_CONFIRM_ENABLE = CONFIG.LOGIN_CONFIRM_ENABLE
OTP_IN_RADIUS = CONFIG.OTP_IN_RADIUS
