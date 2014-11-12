# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Vincent Garonne, <vincent.garonne@cern.ch>, 2012
# - Martin Barisits, <martin.barisits@cern.ch>, 2013-2014
# - Cedric Serfon, <cedric.serfon@cern.ch>, 2014

from rucio.api.permission import has_permission
from rucio.common.exception import AccessDenied
from rucio.common.schema import validate_schema
from rucio.core import rule


def add_replication_rule(dids, copies, rse_expression, weight, lifetime, grouping, account, locked, subscription_id, source_replica_expression, activity, notify, purge_replicas, issuer):
    """
    Adds a replication rule.

    :param dids:                       The data identifier set.
    :param copies:                     The number of replicas.
    :param rse_expression:             Boolean string expression to give the list of RSEs.
    :param weight:                     If the weighting option of the replication rule is used, the choice of RSEs takes their weight into account.
    :param lifetime:                   The lifetime of the replication rules (in seconds).
    :param grouping:                   ALL -  All files will be replicated to the same RSE.
                                       DATASET - All files in the same dataset will be replicated to the same RSE.
                                       NONE - Files will be completely spread over all allowed RSEs without any grouping considerations at all.
    :param account:                    The account owning the rule.
    :param locked:                     If the rule is locked, it cannot be deleted.
    :param subscription_id:            The subscription_id, if the rule is created by a subscription.
    :param source_replica_expression:  Only use replicas from this RSE as sources.
    :param activity:                   Activity to be passed on to the conveyor.
    :param notify:                     Notification setting of the rule.
    :purge purge_replicas:             The purge setting to delete replicas immediately after rule deletion.
    :param issuer:                     The issuing account of this operation.
    :returns:                          List of created replication rules.
    """
    if account is None:
        account = issuer

    kwargs = {'dids': dids, 'copies': copies, 'rse_expression': rse_expression, 'weight': weight, 'lifetime': lifetime,
              'grouping': grouping, 'account': account, 'locked': locked, 'subscription_id': subscription_id,
              'source_replica_expression': source_replica_expression, 'notify': notify, 'activity': activity, 'purge_replicas': purge_replicas}

    validate_schema(name='activity', obj=kwargs['activity'])

    if not has_permission(issuer=issuer, action='add_rule', kwargs=kwargs):
        raise AccessDenied('Account %s can not add replication rule' % (issuer))
    return rule.add_rule(account=account,
                         dids=dids,
                         copies=copies,
                         rse_expression=rse_expression,
                         grouping=grouping,
                         weight=weight,
                         lifetime=lifetime,
                         locked=locked,
                         subscription_id=subscription_id,
                         source_replica_expression=source_replica_expression,
                         activity=activity,
                         notify=notify,
                         purge_replicas=purge_replicas)


def get_replication_rule(rule_id):
    """
    Get replication rule by it's id.

    :param rule_id: The rule_id to get.
    """
    return rule.get_rule(rule_id)


def list_replication_rules(filters={}):
    """
    Lists replication rules based on a filter.

    :param filters: dictionary of attributes by which the results should be filtered.
    """
    return rule.list_rules(filters)


def list_associated_replication_rules_for_file(scope, name):
    """
    Lists associated replication rules by file.

    :param scope: Scope of the file..
    :param name:  Name of the file.
    """
    return rule.list_associated_rules_for_file(scope=scope, name=name)


def delete_replication_rule(rule_id, issuer):
    """
    Deletes a replication rule and all associated locks.

    :param rule_id:  The id of the rule to be deleted
    :param issuer:   The issuing account of this operation
    :raises:         RuleNotFound, AccessDenied
    """
    kwargs = {'rule_id': rule_id}
    if not has_permission(issuer=issuer, action='del_rule', kwargs=kwargs):
        raise AccessDenied('Account %s can not remove this replication rule.' % (issuer))
    rule.delete_rule(rule_id)


def update_replication_rule(rule_id, options, issuer):
    """
    Update lock state of a replication rule.

    :param rule_id:     The rule_id to lock.
    :param options:     Options dictionary.
    :param issuer:      The issuing account of this operation
    :raises:            RuleNotFound if no Rule can be found.
    """
    kwargs = {'rule_id': rule_id, 'options': options}
    if not has_permission(issuer=issuer, action='update_rule', kwargs=kwargs):
        raise AccessDenied('Account %s can not update this replication rule.' % (issuer))
    rule.update_rule(rule_id=rule_id, options=options)
