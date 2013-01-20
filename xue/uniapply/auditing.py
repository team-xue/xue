# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

__all__ = [
        'is_expired',
        'is_auditer',
        'is_class_applicable',
        'get_auditing_status',
        'check_target_user',
        ]

import datetime
from collections import OrderedDict
from itertools import izip

from .models import *


def is_expired(tgt):
    return not (tgt.start_date < datetime.datetime.today() < tgt.end_date)


def is_auditer(rules, user):
    return any(rule.auditer == user for rule in rules)


def is_class_applicable(tgt, user):
    if user.profile.role != 0:
        # not a student, hence no associated logical class
        return False

    # XXX optimize the query
    return user.central_info.klass in tgt.allowed_classes.all()


def get_auditing_status(entry):
    target = entry.target
    rules = AuditingRule.objects.filter(target=target)

    # iterate through the rules
    prioritized_rules = sorted((rule.niceness, rule, ) for rule in rules)
    if not prioritized_rules:
        # no rules defined, pass by default...
        return 1, OrderedDict(), None

    rule_results, statuses = OrderedDict(), []
    for niceness, rule in prioritized_rules:
        try:
            result = AuditOutcome.objects.get(entry=entry, rule=rule)
        except AuditOutcome.DoesNotExist:
            # final result not known yet, i.e. pending
            # add a fake result item to reflect this
            result = None

        rule_results[rule] = result
        statuses.append(result.status if result is not None else 0)

    status = 0
    if all(i == 1 for i in statuses):
        # pass
        status = 1
    elif any(i == 2 for i in statuses):
        # if one outcome fail, the whole application fail
        status = 2

    # get the next rule to be examined
    if status == 1 or status == 2:
        # no more outstanding rules
        next_rule = None
    else:
        for (niceness, rule, ), status in izip(prioritized_rules, statuses, ):
            if status == 0:
                next_rule = rule
                break

    return status, rule_results, next_rule


def check_target_user(target, user):
    if user.is_staff or target.user == user:
        # Superuser can see EVERYTHING; also owner can see his items
        return True, True

    if is_expired(target):
        return False, False

    # cache the rule objects to reduce db impact
    # force the queryset to hit db (no point deferring it anyway)
    rules = list(AuditingRule.objects.filter(target=target))

    if user.profile.role == 0:
        # XXX is student able to become auditer?
        if is_auditer(rules, user):
            return True, True

        # check if its class is relevant
        if not is_class_applicable(target, user):
            return False, False

        # visible but not manageable (for ordinary students)
        return True, False
    else:
        # check if the user is an auditer
        if is_auditer(target, user):
            return True, True

        return False, False

    raise RuntimeError(u'Impossible codepath!')


def get_imm_auditable_rule(entry, user):
    target = entry.target
    rules = AuditingRule.objects.filter(target=target)

    # iterate through the rules
    prioritized_rules = sorted((rule.niceness, rule, ) for rule in rules)
    #for niceness, rule in prioritized_rules:
    #    if rule.auditer
 

# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
