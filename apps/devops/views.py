# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from .forms import TaskForm
from .hands import *

__all__ = ['TaskListView', 'TaskCreateView']

logger = logging.getLogger(__name__)


class TaskListView(LoginRequiredMixin, TemplateView):
    template_name = 'devops/task_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ansible'),
            'action': _('Tasks'),
        }
        kwargs.update(context)
        return super(TaskListView, self).get_context_data(**kwargs)


class TaskCreateView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devops/task_create.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ansible'),
            'action': _('Create Tasks'),
            'form': TaskForm,
        }
        kwargs.update(context)
        return super(TaskCreateView, self).get_context_data(**kwargs)
