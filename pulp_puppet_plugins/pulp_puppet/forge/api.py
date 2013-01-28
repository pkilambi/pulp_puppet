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

import base64
import json
import re

import web

from pulp_puppet.forge import releases

urls = (
    '/releases.json', 'Releases',
)

app = web.application(urls, globals())

# shamelessly borrowed from puppet forge's error message
MODULE_PATTERN = re.compile('\\A[a-zA-Z0-9]+\\/[a-zA-Z0-9_]+\\Z')


class Releases(object):
    def GET(self):
        credentials = self._get_credentials()
        if not credentials:
            return web.unauthorized()

        module_name = self._get_module_name()
        if not module_name:
            # apparently our version of web.py, 0.36, doesn't take a message
            # parameter for error handlers like this one. Ugh.
            return web.badrequest()

        web.header('Content-Type', 'application/json')
        data = releases.view(*credentials, module_name=module_name)
        return json.dumps(data)

    @staticmethod
    def _get_credentials():
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        if auth:
            encoded_credentials = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(encoded_credentials).split(':')
            return username, password

    @staticmethod
    def _get_module_name():
        module_name = web.input().get('module', '')
        if MODULE_PATTERN.match(module_name):
            return module_name


if __name__ == '__main__':
    app.run()
