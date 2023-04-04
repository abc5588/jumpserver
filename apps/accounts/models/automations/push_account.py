from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.const import AutomationTypes
from accounts.models import Account
from jumpserver.utils import has_valid_xpack_license
from .base import AccountBaseAutomation
from .change_secret import ChangeSecretMixin

__all__ = ['PushAccountAutomation']


class PushAccountAutomation(ChangeSecretMixin, AccountBaseAutomation):
    triggers = models.JSONField(max_length=16, default=list, verbose_name=_('Triggers'))
    username = models.CharField(max_length=128, verbose_name=_('Username'))
    action = models.CharField(max_length=16, verbose_name=_('Action'))
    params = models.JSONField(default=dict, verbose_name=_("Params"))

    def create_nonlocal_accounts(self, usernames, asset):
        secret_type = self.secret_type
        account_usernames = asset.accounts.filter(secret_type=self.secret_type).values_list(
            'username', flat=True
        )
        create_usernames = set(usernames) - set(account_usernames)
        create_account_objs = [
            Account(
                name=f'{username}-{secret_type}', username=username,
                secret_type=secret_type, asset=asset,
            )
            for username in create_usernames
        ]
        Account.objects.bulk_create(create_account_objs)

    def set_period_schedule(self):
        pass

    @property
    def dynamic_username(self):
        return self.username == '@USER'

    @dynamic_username.setter
    def dynamic_username(self, value):
        if value:
            self.username = '@USER'

    def save(self, *args, **kwargs):
        self.type = AutomationTypes.push_account
        if not has_valid_xpack_license():
            self.is_periodic = False
        super().save(*args, **kwargs)

    def to_attr_json(self):
        attr_json = super().to_attr_json()
        attr_json.update({
            'username': self.username,
            'params': self.params,
        })
        return attr_json

    def is_params(self):
        return bool(self.params)

    class Meta:
        verbose_name = _("Push asset account")
