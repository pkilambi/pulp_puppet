# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from gettext import gettext as _

from pulp.client.commands.unit import UnitRemoveCommand
from pulp_puppet.common import constants

class RemoveCommand(UnitRemoveCommand):
    DESC = _('remove copied or uploaded modules from a repository')

    def __init__(self, context):
        super(RemoveCommand, self).__init__(
            context,
            name='remove',
            description=self.DESC,
            type_id=constants.TYPE_PUPPET_MODULE,
        )
