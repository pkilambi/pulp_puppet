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

import logging
import subprocess

from pulp.agent.lib import handler
from pulp.agent.lib.report import BindReport, CleanReport, ContentReport


logger = logging.getLogger(__name__)


class ModuleHandler(handler.ContentHandler):
    def install(self, conduit, units, options):
        """
        Install content unit(s).

        :param  conduit: A handler conduit
        :type   conduit: pulp.agent.lib.conduit.Conduit
        :param  units: A list of content unit (keys)
        :type   units: list
        :param  options: Unit install options.
        :type   options: dict

        :return:    An install report.
        :rtype:     pulp.agent.lib.report.ContentReport
        """
        logger.info('installing modules %s' % str(units))
        url = options.get('url')
        return self._perform_operation('install', units, url)

    def update(self, conduit, units, options):
        """
        Update content unit(s).

        :param  conduit: A handler conduit
        :type   conduit: pulp.agent.lib.conduit.Conduit
        :param  units: A list of content unit (keys)
        :type   units: list
        :param  options: Unit update options.
        :type   options: dict
        :return:    An update report.
        :rtype:     pulp.agent.lib.report.ContentReport
        """
        logger.info('installing modules %s' % str(units))
        return self._perform_operation('upgrade', units)

    def uninstall(self, conduit, units, options):
        """
        Uninstall content unit(s).

        :param  conduit: A handler conduit
        :type   conduit: L{pulp.agent.lib.conduit.Conduit
        :param  units: A list of content unit (keys)
        :type   units: list
        :param  options: Unit uninstall options.
        :type   options: dict
        :return:    An uninstall report.
        :rtype:     pulp.agent.lib.report.ContentReport
        """
        logger.info('removing modules %s' % units)
        return self._perform_operation('uninstall', units)

    def profile(self, conduit):
        """
        Request the installed content profile be sent
        to the pulp server.

        :param  conduit: A handler conduit.
        :type   conduit: pulp.agent.lib.conduit.Conduit
        :return:    A profile report.
        :rtype:     pulp.agent.lib.report.ProfileReport
        """
        raise NotImplementedError()

    @staticmethod
    def _perform_operation(operation, units, url=None):
        report = ContentReport()
        for unit in units:
            try:
                args = ['puppet', 'module', operation, '--version', unit['version'], '--ignore-dependencies', '%s/%s' % (unit['author'], unit['name'])]
                if url:
                    args.insert(5, '--module_repository')
                    args.insert(6, url)
                subprocess.check_call(args)
            except subprocess.CalledProcessError:
                report.set_failed()
                return report
        report.set_succeeded()
        return report


class BindHandler(handler.BindHandler):
    def bind(self, conduit, binding, options):
        """
        Bind a repository. This is a no-op since the consumer does not need
        to keep any state with regard to bindings.

        :param  conduit: A handler conduit.
        :type   conduit: pulp.agent.lib.conduit.Conduit
        :param  binding: A binding to add/update.
          A binding is: {type_id:<str>, repo_id:<str>, details:<dict>}
        :type   binding: dict
        :param  options: Bind options.
        :type   options: dict

        :return: A bind report.
        :rtype:  BindReport
        """
        repo_id = binding['repo_id']
        logger.info('binding to repo %s' % repo_id)

        report = BindReport(repo_id)
        report.set_succeeded()
        return report

    def unbind(self, conduit, repo_id, options):
        """
        Unbind a repository. This is a no-op since the consumer does not need
        to keep any state with regard to bindings.

        :param  conduit: A handler conduit.
        :type   conduit:  pulp.agent.lib.conduit.Conduit
        :param  repo_id: A repository ID.
        :type   repo_id: str
        :param  options: Unbind options.
        :type   options: dict

        :return:    An unbind report.
        :rtype:     BindReport
        """
        report = BindReport(repo_id)
        report.set_succeeded()
        return report

    def clean(self, conduit):
        """
        Clean up. This is a no-op since the consumer does not need
        to keep any state with regard to bindings.

        :param  conduit: A handler conduit.
        :type   conduit: pulp.agent.lib.conduit.Conduit

        :return:    A clean report.
        :rtype:     CleanReport
        """
        report = CleanReport()
        report.set_succeeded()
        return report
