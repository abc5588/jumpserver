# -*- coding: utf-8 -*-
#
from typing import Callable

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.db.utils import IntegrityError
from django.db.models.fields import related

from common.exceptions import JMSException
from common.utils.timezone import as_current_tz
from common.db.encoder import ModelJSONFieldEncoder
from common.mixins.models import CommonModelMixin
from orgs.models import Organization
from tickets.const import (
    TicketType, TicketStatus, TicketState,
    TicketLevel, StepState
)
from tickets.handlers import get_ticket_handler
from tickets.errors import AlreadyClosed

__all__ = ['Ticket', 'TicketStep', 'TicketAssignee', 'SuperTicket']


class TicketStep(CommonModelMixin):
    ticket = models.ForeignKey(
        'Ticket', related_name='ticket_steps',
        on_delete=models.CASCADE, verbose_name='Ticket'
    )
    level = models.SmallIntegerField(
        default=TicketLevel.one, choices=TicketLevel.choices,
        verbose_name=_('Approve level')
    )
    state = models.CharField(
        max_length=64, choices=StepState.choices,
        default=StepState.pending, verbose_name=_("State")
    )

    def change_state(self, state):
        self.state = state
        self.save()
        self.ticket.handler.on_step_change(self)

    def _on_active(self):
        self.send_msg_to_assignees()

    def send_msg_to_assignees(self):
        # Todo: send msg
        self.state = TicketState.notified
        self.save()

    def next(self):
        kwargs = dict(ticket=self.ticket, level=self.level+1, status=StepStatus.pending)
        return self.__class__.objects.filter(**kwargs).first()

    def need_next(self):
        return self.state == TicketState.approved

    class Meta:
        verbose_name = _("Ticket step")


class TicketAssignee(CommonModelMixin):
    assignee = models.ForeignKey(
        'users.User', related_name='ticket_assignees',
        on_delete=models.CASCADE, verbose_name='Assignee'
    )
    state = models.CharField(
        choices=TicketState.choices, max_length=64,
        default=TicketState.pending
    )
    step = models.ForeignKey(
        'tickets.TicketStep', related_name='ticket_assignees',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Ticket assignee')

    def __str__(self):
        return '{0.assignee.name}({0.assignee.username})_{0.step}'.format(self)


class StatusMixin:
    State = TicketState
    Status = TicketStatus

    state: str
    status: str
    applicant: models.ForeignKey
    current_step: TicketStep
    save: Callable
    create_process_steps_by_flow: Callable
    create_process_steps_by_assignees: Callable
    assignees: Callable
    set_serial_num: Callable
    handler: None

    def set_state(self, state: TicketState):
        self.state = state

    def set_status(self, status: TicketStatus):
        self.status = status

    def is_state(self, state: TicketState):
        return self.state == state

    def is_status(self, status: TicketStatus):
        return self.status == status

    def open(self, applicant=None):
        self.set_serial_num()
        self.applicant = applicant
        self.create_process_steps_by_flow()
        self._change_state(StepState.pending, applicant)

    def open_by_assignees(self, assignees):
        self.set_serial_num()
        self.create_process_steps_by_assignees(assignees)
        self._change_state(StepState.pending, None)

    def approve(self, processor):
        self._change_state(StepState.approved, processor)

    def reject(self, processor):
        self._change_state(StepState.rejected, processor)

    def close(self, processor):
        self._change_state(StepState.closed, processor)

    def _update_state(self, state, processor):
        if state != TicketState.approved:
            self.state = state
        self.handler.on_state_change(state)

    def _change_state(self, state, processor):
        if self.is_status(self.Status.closed):
            raise AlreadyClosed

        self._update_step_state(state, processor)
        self._update_state(state, processor)

    def _update_step_state(self, state, processor):
        self.current_step.change_state(state)
        self.current_step.ticket_assignees \
            .filter(assignee=processor) \
            .update(state=state)


class Ticket(StatusMixin, CommonModelMixin):
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    type = models.CharField(
        max_length=64, choices=TicketType.choices,
        default=TicketType.general, verbose_name=_('Type')
    )
    state = models.CharField(
        max_length=16, choices=TicketState.choices,
        default=TicketState.pending, verbose_name=_('State')
    )
    status = models.CharField(
        max_length=16, choices=TicketStatus.choices,
        default=TicketStatus.open, verbose_name=_('Status')
    )
    # 申请人
    applicant = models.ForeignKey(
        'users.User', related_name='applied_tickets', on_delete=models.SET_NULL,
        null=True, verbose_name=_("Applicant")
    )
    comment = models.TextField(default='', blank=True, verbose_name=_('Comment'))
    flow = models.ForeignKey(
        'TicketFlow', related_name='tickets', on_delete=models.SET_NULL,
        null=True, verbose_name=_('TicketFlow')
    )
    approval_step = models.SmallIntegerField(
        default=TicketLevel.one, choices=TicketLevel.choices, verbose_name=_('Approval step')
    )
    serial_num = models.CharField(max_length=128, unique=True, null=True, verbose_name=_('Serial number'))
    rel_snapshot = models.JSONField(verbose_name=_('Relation snapshot'), default=dict)
    org_id = models.CharField(
        max_length=36, blank=True, default='', verbose_name=_('Organization'), db_index=True
    )

    class Meta:
        ordering = ('-date_created',)
        verbose_name = _('Ticket')

    def __str__(self):
        return '{}({})'.format(self.title, self.applicant)

    # TODO 先单独处理一下
    @property
    def org_name(self):
        org = Organization.get_instance(self.org_id)
        return org.name

    @property
    def type_apply_asset(self):
        return self.type == TicketType.apply_asset.value

    @property
    def type_apply_application(self):
        return self.type == TicketType.apply_application.value

    @property
    def type_login_confirm(self):
        return self.type == TicketType.login_confirm.value

    @property
    def current_step(self):
        return self.ticket_steps.filter(level=self.approval_step).first()

    @property
    def current_assignees(self):
        ticket_assignees = self.current_step.ticket_assignees.all()
        return [i.assignee for i in ticket_assignees]

    @property
    def processor(self):
        processor = self.current_step.ticket_assignees \
            .exclude(state=StepState.pending) \
            .first()
        return processor.assignee if processor else None

    @property
    def process_map(self):
        process_map = []
        steps = self.ticket_steps.all()
        for step in steps:
            assignee_ids = []
            assignees_display = []
            ticket_assignees = step.ticket_assignees.all()
            processor = None
            state = step.state
            for i in ticket_assignees:
                assignee_ids.append(i.assignee.id)
                assignees_display.append(str(i.assignee))
                if state != StepState.pending and state == i.state:
                    processor = i.assignee
            step_info = {
                'state': state,
                'approval_level': step.level,
                'assignees': assignee_ids,
                'assignees_display': assignees_display,
                'approval_date': str(step.date_updated),
                'processor': processor.id if processor else '',
                'processor_display': str(processor) if processor else ''
            }
            process_map.append(step_info)
        return process_map

    def exclude_applicant(self, assignees, applicant=None):
        applicant = applicant if applicant else self.applicant
        if len(assignees) != 1:
            assignees = set(assignees) - {applicant, }
        return list(assignees)

    def create_process_steps_by_flow(self):
        org_id = self.flow.org_id
        flow_rules = self.flow.rules.order_by('level')
        for rule in flow_rules:
            step = TicketStep.objects.create(ticket=self, level=rule.level)
            assignees = rule.get_assignees(org_id=org_id)
            assignees = self.exclude_applicant(assignees, self.applicant)
            step_assignees = [TicketAssignee(step=step, assignee=user) for user in assignees]
            TicketAssignee.objects.bulk_create(step_assignees)

    def create_process_steps_by_assignees(self, assignees):
        assignees = self.exclude_applicant(assignees, self.applicant)
        step = TicketStep.objects.create(ticket=self, level=1)
        ticket_assignees = [TicketAssignee(step=step, assignee=user) for user in assignees]
        TicketAssignee.objects.bulk_create(ticket_assignees)

    def has_current_assignee(self, assignee):
        return self.ticket_steps.filter(
            ticket_assignees__assignee=assignee,
            level=self.approval_step
        ).exists()

    def has_all_assignee(self, assignee):
        return self.ticket_steps.filter(ticket_assignees__assignee=assignee).exists()

    @classmethod
    def get_user_related_tickets(cls, user):
        queries = Q(applicant=user) | Q(ticket_steps__ticket_assignees__assignee=user)
        tickets = cls.objects.all().filter(queries).distinct()
        return tickets

    def get_current_ticket_flow_approve(self):
        return self.flow.rules.filter(level=self.approval_step).first()

    @classmethod
    def all(cls):
        return cls.objects.all()

    def set_rel_snapshot(self, save=True):
        rel_fields = set()
        m2m_fields = set()
        for name, field in self._meta._forward_fields_map.items():
            if isinstance(field, related.RelatedField):
                rel_fields.add(name)
            if isinstance(field, related.ManyToManyField):
                m2m_fields.add(name)

        snapshot = {}
        for field in rel_fields:
            value = getattr(self, field)

            if field in m2m_fields:
                value = [str(v) for v in value.all()]
            else:
                value = str(value) if value else ''
            snapshot[field] = value

        self.rel_snapshot = snapshot
        if save:
            self.save(update_fields=('rel_snapshot',))

    @property
    def handler(self):
        return get_ticket_handler(ticket=self)

    @property
    def body(self):
        _body = self.handler.get_body()
        return _body

    def get_next_serial_num(self):
        date_created = as_current_tz(self.date_created)
        date_prefix = date_created.strftime('%Y%m%d')

        ticket = Ticket.objects.all().select_for_update().filter(
            serial_num__startswith=date_prefix
        ).order_by('-date_created').first()

        last_num = 0
        if ticket:
            last_num = ticket.serial_num[8:]
            last_num = int(last_num)
        num = '%04d' % (last_num + 1)
        # 202212010001
        return '{}{}'.format(date_prefix, num)

    def set_serial_num(self):
        if self.serial_num:
            return

        try:
            self.serial_num = self.get_next_serial_num()
            self.save(update_fields=('serial_num',))
        except IntegrityError as e:
            if e.args[0] == 1062:
                # 虽然做了 `select_for_update` 但是每天的第一条工单仍可能造成冲突
                # 但概率小，这里只报错，用户重新提交即可
                raise JMSException(detail=_('Please try again'), code='please_try_again')
            raise e


class SuperTicket(Ticket):
    class Meta:
        proxy = True
        verbose_name = _("Super ticket")
