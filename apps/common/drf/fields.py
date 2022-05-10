# -*- coding: utf-8 -*-
#

from rest_framework import serializers

from common.utils import rsa_decrypt_by_session_pkey

__all__ = [
    'ReadableHiddenField', 'EncryptedField'
]


# ReadableHiddenField
# -------------------


class ReadableHiddenField(serializers.HiddenField):
    """ 可读的 HiddenField """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_only = False

    def to_representation(self, value):
        if hasattr(value, 'id'):
            return getattr(value, 'id')
        return value


class EncryptedField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, value):
        value = super().to_internal_value(value)
        return rsa_decrypt_by_session_pkey(value)
