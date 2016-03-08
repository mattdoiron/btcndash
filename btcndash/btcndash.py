#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014. All rights reserved.

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
 * bitcoinrpc: rpc library (https://github.com/jgarzik/python-bitcoinrpc)
 * Blocks: bootstrap theme (http://alvarez.is/demo/free/blocks/)

Donate Bitcoin to 1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM

:copyright: (c) 2014 by Matt Doiron.
:license: GPL v3, see LICENSE for more details.
"""

__title__ = "BTCnDash"
__author__ = "Matt Doiron"
__copyright__ = "Copyright 2014, Matt Doiron"
__license__ = "GPL v3"
__version__ = "1.0.0"
__maintainer__ = "Matt Doiron"
__email__ = "mattdoiron@gmail.com"
__status__ = "Development"

# TODO save data transferred, uptime persistently
# TODO test init scripts (both types init.d and upstart)
# TODO clean up css files (lots of unused stuff)
# TODO refactor to reduce duplicate code


# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import time
import os
import threading
import atexit
import urllib
import json
import errno
from socket import error as socket_error

from bottle import Bottle, template, static_file, TEMPLATE_PATH
from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoinrpc.authproxy import JSONRPCException


# ----------------------------------------------------
# Constants
# ----------------------------------------------------

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(APP_ROOT, 'views'))
PAGES = {'index': {'template': 'index.tpl',
                   'static': 'index.html'},
         'peers': {'template': 'peers.tpl',
                   'static': 'peers.html'},
         'tx':    {'template': 'tx.tpl',
                   'static': 'tx.html'},
         '404':   {'template': '404.tpl',
                   'static': '404.html'}}

# ----------------------------------------------------
# Create Bottle App and Load Configuration File
# ----------------------------------------------------

app = Bottle()
app.config.load_config(os.path.join(APP_ROOT, 'btcndash.conf'))

# RPC and Node settings
RPC_URN = app.config['bitcoind.rpc_urn']
NODE_PORT = app.config['bitcoind.node_port']

# BTCnDash settings
DONATE_ADDRESS = app.config['btcndash.donate_address']
CACHE_TIME = int(app.config['btcndash.cache_time'])
CACHE_TIME_LOC = int(app.config['btcndash.cache_time_location'])
SERVER_IP_LOCAL = app.config['btcndash.ip_local']
SERVER_IP_PUBLIC = app.config['btcndash.ip_public']
SERVER_PORT = app.config['btcndash.port']
SERVER_TYPE = app.config['btcndash.server_type']
SERVER_LOCATION = app.config['btcndash.server_location']
DEBUG = True if app.config['btcndash.debug'] == 'True' else False

# External API settings
QR_URL = app.config['api.qr_url']
QR_PARAM = app.config['api.qr_parameter']
BLOCK_HEIGHT_URL = app.config['api.block_height_url']
IP_INFO_URL = app.config['api.ip_info_url']
TX_INFO_URL = app.config['api.tx_info_url']
HASH_DIFF_URL = app.config['api.hash_diff_url']
LOC_URL = app.config['api.location_url']
MAP_URL = app.config['api.map_url']
DONATE_URL = app.config['api.donate_url']


# ----------------------------------------------------
# Page Cache Class
# ----------------------------------------------------

class PageCache(object):
    """Takes care of getting and caching pages of different types."""

    def __init__(self):
        """Upon init, refresh cached pages"""

        # Fetch and cache all pages
        for page in PAGES.keys():
            self.cache_page(page)

    @staticmethod
    def cache_loc():
        """Cache location/IP separately because they should rarely change."""

        # Refresh IP and location
        try:
            global SERVER_IP_PUBLIC
            global SERVER_LOCATION
            global MAP_URL
            loc = json.loads(urllib.urlopen(LOC_URL).read())
            SERVER_LOCATION = ', '.join([loc['city'],
                                         loc['region'],
                                         loc['country']])
            SERVER_IP_PUBLIC = loc['query']
            MAP_URL = MAP_URL.format(loc['lat'], loc['lon'])
        except (IOError, ValueError) as e:
            print "Error: {}".format(e)
            SERVER_IP_PUBLIC = 'n/a'
            SERVER_LOCATION = 'Unknown'
            MAP_URL = '#'

    @staticmethod
    def cache_404():
        """Creates a static 404 page"""
        return {'title': 'BTCnDash: Error 404 - Page not found',
                'donate': DONATE_ADDRESS,
                'donate_url': DONATE_URL + DONATE_ADDRESS}

    @staticmethod
    def cache_index():
        """Takes care of getting and caching the index page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            info = rpc.getinfo()
            netinfo = rpc.getnettotals()
            sent = netinfo['totalbytessent']
            recv = netinfo['totalbytesrecv']
            total = sent + recv
            hashrate = float(rpc.getnetworkhashps())
            transactions = rpc.getrawmempool()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered the "
                                 "correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            info = {'connections': None, 'blocks': 0, 'difficulty': 0, 'version': 'n/a'}
            sent = 0
            recv = 0
            total = 0.0000001
            hashrate = 0.0
            transactions = []

        # Collect, format and return the required data in a dict
        return {'cons': info['connections'],
                'hashrate': '{:,.1f}'.format(hashrate / 1.0E12),
                'block_height': '{:,}'.format(info['blocks']),
                'block_url': BLOCK_HEIGHT_URL + str(info['blocks']),
                'diff': '{:,.2f}'.format(info['difficulty']),
                'version': info['version'],
                'sent': '{:,.1f}'.format(sent / 1048576.0),
                'recv': '{:,.1f}'.format(recv / 1048576.0),
                'total': '{:,.3f}'.format(total / 1073741824.0),
                'pcnt_in': '{:,.1f}'.format(recv / float(total) * 100.0),
                'pcnt_out': '{:,.1f}'.format(sent / float(total) * 100.0),
                'tx': transactions,
                'tx_count': '{:,}'.format(len(transactions)),
                'update': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ip': ':'.join([SERVER_IP_PUBLIC, NODE_PORT]),
                'loc': SERVER_LOCATION,
                'donate': DONATE_ADDRESS,
                'donate_url': DONATE_URL + DONATE_ADDRESS,
                'qr_url': QR_URL + QR_PARAM + DONATE_ADDRESS,
                'title': 'Bitcoin Node Status',
                'map_url': MAP_URL,
                'hash_diff_url': HASH_DIFF_URL}

    @staticmethod
    def cache_peers():
        """Takes care of getting and caching the peers page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            peers = rpc.getpeerinfo()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered "
                                 "the correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            peers = []

        # Collect, format and return the required data in a dict
        return {'peers': peers,
                'node_url': IP_INFO_URL,
                'title': 'Bitcoin Node Status - Peers',
                'donate': DONATE_ADDRESS,
                'donate_url': DONATE_URL + DONATE_ADDRESS}

    @staticmethod
    def cache_tx():
        """Takes care of getting and caching the transactions page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            tx = rpc.getrawmempool()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered "
                                 "the correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            tx = []

        # Collect, format and return the required data in a dict
        return {'transactions': tx,
                'tx_url': TX_INFO_URL,
                'title': 'Bitcoin Node Status - Transactions',
                'donate': DONATE_ADDRESS,
                'donate_url': DONATE_URL + DONATE_ADDRESS}

    def cache_page(self, _page):
        """Gets and caches the specified page."""

        # Retrieve the dictionary containing info about the page
        page = PAGES.get(_page, 'index')

        # Find the last modified time of the STATIC_PAGE and the current time
        now = time.time()
        if os.path.exists(page['static']):
            modified = os.path.getmtime(page['static'])
        else:
            modified = False

        # Check if last modified time is > CACHE_TIME_LOC seconds ago
        if now - modified >= CACHE_TIME_LOC or not modified:

            # Refresh location and ip before checking other pages
            self.cache_loc()

        # Check if last modified time is > CACHE_TIME seconds ago
        if now - modified >= CACHE_TIME or not modified:

            # Retrieve the specified data
            data = getattr(self, 'cache_' + _page)()

            # Open the static file and write the compiled template
            if data:
                path = os.path.join(APP_ROOT, 'static', 'html', page['static'])
                with open(path, 'wb') as static_page:
                    static_page.write(template(page['template'], data=data))


# ----------------------------------------------------
# Worker Class to Refresh Page Cache in Background
# ----------------------------------------------------

class Worker(object):
    """Creates the worker thread, which refreshes the page cache"""

    def __init__(self):
        """Immediately refresh the cache"""
        print 'Launching worker...'
        self.refresh_cache()

    @staticmethod
    def interrupt():
        global worker_thread
        worker_thread.cancel()

    def refresh_cache(self):
        global worker_thread

        # Call PageCache object to check cache freshness
        PageCache()

        try:
            # Set the next thread to start in cache_time seconds
            worker_thread = threading.Timer(CACHE_TIME, self.refresh_cache, ())
            worker_thread.daemon = True
            worker_thread.start()

            # When you kill Bottle (SIGTERM), clear the next timer
            atexit.register(self.interrupt)

        except (KeyboardInterrupt, SystemExit):
            self.interrupt()


# ----------------------------------------------------
# Bottle Routes
# ----------------------------------------------------

@app.route('/')
@app.route('/<_page>')
@app.route('/<_page>/')
def index(_page=None):
    """Default route to display cached status pages."""
    if _page == 'donate':
        return DONATE_ADDRESS

    page_dict = PAGES.get(_page or 'index', PAGES['404'])
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
    path = os.path.join('static', 'html', PAGES['404']['static'])
    return static_file(path, root=APP_ROOT)


# ----------------------------------------------------
# Start your engines!
# ----------------------------------------------------

if __name__ == '__main__':

    print 'Launching BTCnDash...'

    # Make sure the html cache folder is present
    html_path = os.path.join(APP_ROOT, 'static', 'html')
    try:
        os.makedirs(html_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Create a global thread for the worker
    worker_thread = threading.Thread()

    # Start the worker thread (this also creates the first cache)
    Worker()

    try:
        # Starts the Bottle server with the specified settings
        app.run(host=SERVER_IP_LOCAL, port=SERVER_PORT,
                server=SERVER_TYPE, debug=DEBUG)
    except socket_error as e:
        print 'Unable to start server: {}'.format(e)
