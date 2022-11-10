# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals
from django.views.generic import RedirectView
from django.shortcuts import reverse, redirect
from django.utils.translation import ugettext as _
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core.cache import cache

from users.notifications import ResetPasswordSuccessMsg
from common.utils import get_object_or_none, FlashMessageUtil, random_string
from common.utils.verify_code import SendAndVerifyCodeUtil
from ...models import User
from ...utils import (
    get_password_check_rules, check_password_rules,
)
from ... import forms


__all__ = [
    'UserLoginView', 'UserResetPasswordView', 'UserForgotPasswordView',
    'UserForgotPasswordPreviewingView'
]


class UserLoginView(RedirectView):
    url = reverse_lazy('authentication:login')
    query_string = True


class UserForgotPasswordPreviewingView(FormView):
    template_name = 'users/forgot_password_previewing.html'
    form_class = forms.UserForgotPasswordPreviewingForm

    @staticmethod
    def get_redirect_url(token):
        return reverse('authentication:forgot-password') + '?token=%s' % token

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = get_object_or_none(User, username=username)
        if not user:
            form.add_error('username', _('User does not exist: {}').format(username))
            return super().form_invalid(form)

        token = random_string(36)
        cache.set(token, username, 5 * 60)
        return redirect(self.get_redirect_url(token))


class UserForgotPasswordView(FormView):
    template_name = 'users/forgot_password.html'
    form_class = forms.UserForgotPasswordForm

    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        username = cache.get(token)
        if not username:
            return redirect(self.get_redirect_url(return_previewing=True))
        else:
            return super().get(request, *args, **kwargs)

    @staticmethod
    def get_validate_backends_context():
        validate_backends = [
            {'name': _('Email'), 'is_active': True, 'value': 'email'}
        ]
        if settings.XPACK_ENABLED:
            if settings.SMS_ENABLED:
                is_active = True
            else:
                is_active = False
            sms_backend = {'name': _('SMS'), 'is_active': is_active, 'value': 'sms'}
            validate_backends.append(sms_backend)
        return {'validate_backends': validate_backends}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        if getattr(form, 'errors', None):
            e = getattr(form, 'errors')
            context['errors'] = e
        context['form_type'] = 'email'
        context['XPACK_ENABLED'] = settings.XPACK_ENABLED
        cleaned_data = getattr(form, 'cleaned_data', {})
        for k, v in cleaned_data.items():
            if v:
                context[k] = v
        validate_backends = self.get_validate_backends_context()
        context.update(validate_backends)
        return context

    @staticmethod
    def get_redirect_url(user=None, return_previewing=False):
        if not user and return_previewing:
            return reverse('authentication:forgot-previewing')
        query_params = '?token=%s' % user.generate_reset_token()
        reset_password_url = reverse('authentication:reset-password')
        return reset_password_url + query_params

    def form_valid(self, form):
        token = self.request.GET.get('token')
        username = cache.get(token)
        form_type = form.cleaned_data['form_type']
        code = form.cleaned_data['code']
        target = form.cleaned_data[form_type]
        try:
            sender_util = SendAndVerifyCodeUtil(target, backend=form_type)
            sender_util.verify(code)
        except Exception as e:
            form.add_error('code', str(e))
            return super().form_invalid(form)

        query_key = 'phone' if form_type == 'sms' else form_type
        user = get_object_or_none(User, **{'username': username, query_key: target})
        if not user:
            form.add_error('username', _('User does not exist: {}').format(username))
            return super().form_invalid(form)

        return redirect(self.get_redirect_url(user))


class UserResetPasswordView(FormView):
    template_name = 'users/reset_password.html'
    form_class = forms.UserTokenResetPasswordForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        errors = kwargs.get('errors')
        if errors:
            context['errors'] = errors
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        user = User.validate_reset_password_token(token)
        if not user:
            context['errors'] = _('Token invalid or expired')
            context['token_invalid'] = True
        else:
            check_rules = get_password_check_rules(user)
            context['password_check_rules'] = check_rules
        return context

    def form_valid(self, form):
        token = self.request.GET.get('token')
        user = User.validate_reset_password_token(token)
        if not user:
            error = _('Token invalid or expired')
            form.add_error('new_password', error)
            return self.form_invalid(form)

        if not user.can_update_password():
            error = _('User auth from {}, go there change password')
            form.add_error('new_password', error.format(user.get_source_display()))
            return self.form_invalid(form)

        password = form.cleaned_data['new_password']
        is_ok = check_password_rules(password, is_org_admin=user.is_org_admin)
        if not is_ok:
            error = _('* Your password does not meet the requirements')
            form.add_error('new_password', error)
            return self.form_invalid(form)

        if user.is_history_password(password):
            limit_count = settings.OLD_PASSWORD_HISTORY_LIMIT_COUNT
            error = _('* The new password cannot be the last {} passwords').format(limit_count)
            form.add_error('new_password', error)
            return self.form_invalid(form)

        user.reset_password(password)
        User.expired_reset_password_token(token)

        ResetPasswordSuccessMsg(user, self.request).publish_async()
        url = self.get_redirect_url()
        return redirect(url)

    @staticmethod
    def get_redirect_url():
        message_data = {
            'title': _('Reset password success'),
            'message': _('Reset password success, return to login page'),
            'redirect_url': reverse('authentication:login'),
            'auto_redirect': True,
        }
        return FlashMessageUtil.gen_message_url(message_data)
