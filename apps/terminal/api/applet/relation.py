from typing import Callable

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response

from common.api import JMSModelViewSet
from common.permissions import IsServiceAccount
from common.exceptions import JMSObjectDoesNotExist
from common.utils import is_uuid
from orgs.utils import tmp_to_builtin_org
from rbac.permissions import RBACPermission
from terminal.models import AppletHost
from terminal.serializers import (
    AppletHostAccountSerializer,
    AppletPublicationSerializer,
    AppletHostAppletReportSerializer,
)


class HostMixin:
    request: Request
    permission_denied: Callable
    kwargs: dict
    rbac_perms = (
        ('list', 'terminal.view_applethost'),
        ('retrieve', 'terminal.view_applethost'),
    )

    def get_permissions(self):
        if self.kwargs.get('host') and settings.DEBUG:
            return [RBACPermission()]
        else:
            return [IsServiceAccount()]

    def self_host(self):
        try:
            return self.request.user.terminal.applet_host
        except AttributeError:
            raise self.permission_denied(self.request, 'User has no applet host')

    def pk_host(self):
        return get_object_or_404(AppletHost, id=self.kwargs.get('host'))

    @property
    def host(self):
        if self.kwargs.get('host'):
            return self.pk_host()
        else:
            return self.self_host()


class AppletHostAccountsViewSet(HostMixin, JMSModelViewSet):
    serializer_class = AppletHostAccountSerializer

    def get_queryset(self):
        with tmp_to_builtin_org(system=1):
            queryset = self.host.accounts.all()
        return queryset


class AppletHostAppletViewSet(HostMixin, JMSModelViewSet):
    host: AppletHost
    serializer_class = AppletPublicationSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not is_uuid(pk):
            obj = self.host.publications.get(applet__name=pk)
        else:
            obj = self.host.publications.get(pk=pk)
        if not obj.applet.can_show:
            msg = 'You do not have permission on this resource'
            raise self.permission_denied(self.request, msg)
        return obj

    def get_queryset(self):
        queryset = [
            p for p in self.host.publications.all() if not p.applet.can_show
        ]
        return queryset

    @action(methods=['post'], detail=False)
    def reports(self, request, *args, **kwargs):
        serializer = AppletHostAppletReportSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.host.check_applets_state(data)
        publications = self.host.publications.all()
        serializer = AppletPublicationSerializer(publications, many=True)
        return Response(serializer.data)
