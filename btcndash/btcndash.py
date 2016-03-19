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

# ----------------------------------------------------
# Imports
# ----------------------------------------------------

# System Imports
import os
import sys
import argparse
import json
from socket import error as socket_error
from bottle import Bottle, static_file, TEMPLATE_PATH

# BTCnDash Imports
import logger
import worker


# ----------------------------------------------------
# Do Initial Setup and Create Bottle App
# ----------------------------------------------------

def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', nargs='?', default='config.json')
    return parser.parse_known_args()

# Parse command-line arguments
parsed_args, unparsed_args = process_args()
args = sys.argv[:1] + unparsed_args

try:
    with open(parsed_args.config) as config_file:
        config = json.load(config_file)
except IOError:
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
    except IOError as err:
        raise IOError('Cannot find or read config file!')

app = Bottle()
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(APP_ROOT, 'views'))
TEMPLATE_PATH.insert(0, config['alternate_views'])
log = logger.setup_logging(config['log_level'], 'BTCnDash')

# ----------------------------------------------------
# Bottle Routes
# ----------------------------------------------------

@app.route('/')
@app.route('/<_page>')
@app.route('/<_page>/')
def index(_page=None):
    """Default route to display cached status pages."""
    if _page == 'donate':
        return config['donate_address']

    page_dict = config['pages'].get(_page or 'index', config['pages']['404'])
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
    path = os.path.join('static', 'html', config['pages']['404']['static'])
    return static_file(path, root=APP_ROOT)

# ----------------------------------------------------
# Start your engines!
# ----------------------------------------------------


def main():

    log.info('Launching BTCnDash...')

    # Start the worker thread (this also creates the first cache)
    worker_class = worker.Worker(config)

    try:
        # Starts the Bottle server with the specified settings
        app.run(host=config['server_ip_local'], port=config['server_port'],
                server=config['server_type'], debug=config['debug'])
    except socket_error as err:
        log.error('Unable to start server: {}'.format(err))

if __name__ == '__main__':
    main()
