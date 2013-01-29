# -*- coding: utf-8 -*-
#
# Copyright © 2013 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from pulp.server.db.model.criteria import UnitAssociationCriteria
from pulp.server.managers.consumer.bind import BindManager
from pulp.server.managers.content.query import ContentQueryManager
from pulp.server.managers.repo.unit_association_query import RepoUnitAssociationQueryManager

from pulp_puppet.common.constants import TYPE_PUPPET_MODULE

NULL_AUTH_VALUE = '.'

def view(consumer_id, repo_id, module_name, version):
    if repo_id == NULL_AUTH_VALUE:
        if consumer_id == NULL_AUTH_VALUE:
            return {}
        repo_ids = get_bound_repos(consumer_id)
    else:
        repo_ids = [repo_id]

    units_by_repo = {}
    for repo_id in repo_ids:
        criteria = build_criteria(module_name, version)

        associations = RepoUnitAssociationQueryManager.find_by_criteria(criteria)
        unit_ids = (association['unit_id'] for association in associations)
        # TODO specify fields in the below call
        units = ContentQueryManager.get_multiple_units_by_ids(TYPE_PUPPET_MODULE, unit_ids)
        units_by_repo[repo_id] = units

    # find repo with most recent version
    # create tree within that repo only

    return {}

def unit_to_dict(unit):
    return {
        '%s/%s' % (unit['author'], unit['name']) : {
            'file' : '', # TODO
            'version' : unit['version'],
            'dependencies' : unit['dependencies']
        },
    }


def find_newest(units):
    newest = None
    newest_version = (0,0,0)
    for unit in units:
        version = map(int, unit['version'].split('.'))
        if version > newest_version:
            newest = unit
            newest_version = version
    return newest



def get_bound_repos(consumer_id):
    bindings = BindManager.find_by_consumer(consumer_id)
    repos = [binding['repo_id'] for binding in bindings]
    return repos


def build_criteria(module_name, version):
    author, name = module_name.split('/', 1)

    unit_filters = {
        'name' : name,
        'author' : author,
    }
    if version:
        unit_filters['version'] = version

    criteria = UnitAssociationCriteria(
        type_ids=[TYPE_PUPPET_MODULE],
        unit_filters = unit_filters,
    )
    return criteria

