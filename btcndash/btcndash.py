#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014, Matt Doiron. All rights reserved.

BTCnDash is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BTCnDash is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BTCnDash. If not, see <http://www.gnu.org/licenses/>.
"""

"""
BTCnDash: Python script to generate and server status dashboard
of a full Bitcoin node

Acknowledgments:
 * Bottle: python web framework (http://bottlepy.org)
 * bitcoinlib: rpc library (https://github.com/petertodd/python-bitcoinlib/)
 * Blocks: bootstrap theme (http://alvarez.is/)

Donate Bitcoin to 1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM

:copyright: (c) 2014 by Matt Doiron.
:license: GPL v3, see LICENSE for more details.
"""

__title__ = "BTCnDash"
__author__ = "Matt Doiron"
__copyright__ = "Copyright 2014, Matt Doiron"
__license__ = "GPL v3"
__version__ = "0.1.1"
__maintainer__ = "Matt Doiron"
__email__ = "mattdoiron@gmail.com"
__status__ = "Development"


# ----------------------------------------------------
# Imports
# ----------------------------------------------------

# System Imports
import os
from socket import error as socket_error
from bottle import Bottle, static_file, TEMPLATE_PATH

# BTCnDash Imports
import config
import logger
import worker

# ----------------------------------------------------
# Create Bottle App and Do Initial Setup
# ----------------------------------------------------

app = Bottle()
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(APP_ROOT, 'views'))
log = logger.setup_logging(config.LOG_LEVEL, 'BTCnDash')

# ----------------------------------------------------
# Bottle Routes
# ----------------------------------------------------

@app.route('/')
@app.route('/<_page>')
@app.route('/<_page>/')
def index(_page=None):
    """Default route to display cached status pages."""
    if _page == 'donate':
        return config.DONATE_ADDRESS

    page_dict = config.PAGES.get(_page or 'index', config.PAGES['404'])
    path = os.path.join('static', 'html', page_dict['static'])
    return static_file(path, root=APP_ROOT)


@app.route('favicon.ico')
def favicon():
    path = os.path.join('static', 'img', 'favicon.ico')
    return static_file(path, root=APP_ROOT)


@app.route('/static/<filename:path>')
def static(filename):
    root = os.path.join(APP_ROOT, 'static')
    return static_file(filename, root=root)


@app.error(404)
def error(page=None):
    path = os.path.join('static', 'html', config.PAGES['404']['static'])
    return static_file(path, root=APP_ROOT)

# ----------------------------------------------------
# Start your engines!
# ----------------------------------------------------

if __name__ == '__main__':

    log.info('Launching BTCnDash...')

    # Start the worker thread (this also creates the first cache)
    worker = worker.Worker()

    try:
        # Starts the Bottle server with the specified settings
        app.run(host=config.SERVER_IP_LOCAL, port=config.SERVER_PORT,
                server=config.SERVER_TYPE, debug=config.DEBUG)
    except socket_error as err:
        log.error('Unable to start server: {}'.format(err))
